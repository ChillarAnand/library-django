import importlib
import sys

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.core.management import call_command
from django.db import models
from django.shortcuts import redirect
from django.utils.html import format_html

from book.models import Author
from book.models import BestSeller
from book.models import Book

try:
    from django.urls import reverse
except ImportError:
    # django < 2
    from django.core.urlresolvers import reverse

from crm.models import House


def toggle_book_availability(modeladmin, request, queryset):
    for item in queryset:
        item.is_available = not item.is_available
        item.save()


class BookAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    # autocomplete_fields = ['author']
    actions = [toggle_book_availability]

    list_display = ('name', 'author', 'delete', )
    list_display = ('name', 'author', 'author_link', 'delete', 'borrowed', 'is_available', 'toggle_availability')

    list_display_links = ('name', 'author',)

    def author_link(self, book):
        if not book.author:
            return
        link = reverse("admin:book_author_change", args=[book.author.id])
        html = '<a href="{}">{}</a>'.format(link, book.author.name)
        return format_html(html)
    author_link.short_description = 'Author'

    def delete(self, book):
        link = reverse("admin:book_book_delete", args=[book.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
        return format_html(html)
    delete.short_description = 'Delete'

    def toggle_availability(self, book):
        link = reverse('admin:book-availability-toggle', args=[book.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Toggle" />'.format(link)
        return format_html(html)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^(?P<book_id>.+)/availability-toggle$',
                self.admin_site.admin_view(self.toggle_book_availability), name='book-availability-toggle',
                ),
        ]
        return urls + custom_urls

    def toggle_book_availability(self, request, book_id, *args, **kwargs):
        book = self.get_object(request, book_id)
        book.is_available = not book.is_available
        book.save()
        return redirect(reverse("admin:book_book_changelist"))


admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'active')


admin.site.register(Author, AuthorAdmin)


class HouseAdmin(admin.ModelAdmin):
    def url_for_result(self, house):
        html_string = format_html(u'<a href="/admin/crm/house/{}/change/">{}', house.id, house.id)
        return html_string

    list_display = ('id', 'url_for_result', 'id', )


admin.site.register(House, HouseAdmin)


def get_models(database):
    filename = '/tmp/models.py'
    stdout_backup, sys.stdout = sys.stdout, open(filename, 'w+')
    # with open(filename, 'w') as fh:
    call_command('inspectdb', database=database)
    sys.stdout = stdout_backup
    return filename


def import_module(models_file):
    pass


new_app_name = "my_new_app"

settings.INSTALLED_APPS += (new_app_name,)
# apps.app_configs = OrderedDict()
# apps.ready = False
# apps.populate(settings.INSTALLED_APPS)

database = 'legacy_db'


def load_dynamic_admin(database):
    models_file = get_models(database)
    spec = importlib.util.spec_from_file_location("trash.models", models_file)
    # spec = importlib.util.spec_from_file_location("my_new_app.models", models_file)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)


load_dynamic_admin(database)


def get_related_field(name, admin_order_field=None, short_description=None):
    """
    Create a function that can be attached to a ModelAdmin to use as a list_display field, e.g:
    client__name = getter_for_related_field('client__name', short_description='Client')
    """
    related_names = name.split('__')

    def dynamic_attribute(obj):
        for related_name in related_names:
            obj = getattr(obj, related_name)
            return obj

    dynamic_attribute.admin_order_field = admin_order_field or name
    dynamic_attribute.short_description = short_description or related_names[-1].title().replace('_', ' ')
    return dynamic_attribute


class RelatedFieldAdmin(admin.ModelAdmin):
    '''
    Class
    '''

    def __getattr__(self, attr):
        if '__' in attr:
            return get_related_field(attr)

        # not dynamic lookup, default behaviour
        return self.__getattribute__(attr)

    def get_queryset(self, request):
        qs = super(RelatedFieldAdmin, self).get_queryset(request)

        select_related = [field.rsplit('__', 1)[0] for field in self.list_display if '__' in field]

        model = qs.model
        for field_name in self.list_display:
            try:
                field = model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                continue
            try:
                remote_field = field.remote_field
            except AttributeError:  # for Django<1.9
                remote_field = field.rel
            if isinstance(remote_field, models.ManyToOneRel):
                select_related.append(field_name)

        return qs.select_related(*select_related)


class BestSellerAdmin(RelatedFieldAdmin):
    list_display = ('book', 'book__author', 'book__author__name')

    # list_display = ('book', 'book__author')
    # book_author = get_related_field('book__author')


admin.site.register(BestSeller, BestSellerAdmin)
