import importlib
import sys

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.core.management import call_command
from django.db import models
from django.shortcuts import redirect
from django.utils.html import format_html
from django_otp.admin import OTPAdminSite

from book.models import Author
from book.models import BestSeller
from book.models import Book
from book.models import BookProxy
from advanced_filters.admin import AdminAdvancedFiltersMixin


try:
    from django.urls import reverse
except ImportError:
    # django < 2
    from django.core.urlresolvers import reverse


class LibraryAdminSite(OTPAdminSite):
    pass


# admin_site = LibraryAdminSite()

# admin.site.__class__ = OTPAdminSite


# class LibraryAdminSite(AdminSite):
#     def get_app_list(self, request):
#         """
#         Return a sorted list of all the installed apps that have been
#         registered in this site.
#         """
#         ordering = {
#             "Library": 1,
#             "Book": 4
#         }
#         app_dict = self._build_app_dict(request)
#         app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
#
#         pprint(app_list)
#         # Sort the models alphabetically within each app.
#         for app in app_list:
#             app['models'].sort(key=lambda x: ordering[x['name']])
#
#         return app_list
#
# admin_site = LibraryAdminSite()
admin_site = admin


def make_books_available(modeladmin, request, queryset):
    queryset.update(is_available=True)


make_books_available.short_description = "Mark selected books as available"


def make_books_unavailable(modeladmin, request, queryset):
    queryset.update(is_available=False)

class BookAdmin(admin.ModelAdmin):
    # list_editable = ('author', 'name', 'is_available')

    search_fields = ('name',)
    # autocomplete_fields = ['author']
    actions = ('make_books_available',)

    list_display = ('name', 'author', 'delete', )
    list_display = (
        'name', 'author', 'is_available', 'delete', 'borrowed', 'is_available', 'toggle_availability', 'author_link')
    list_display = (
        'id', 'name', 'author',
        # 'is_available', 'delete',
        # 'author',
        'author', 'author', 'author', 'author', 'author',
    )

    list_display_links = ('name', 'author',)
    list_display_links = ('id',)

    def delete(self, obj):
        view_name = "admin:{}_{}_delete".format(obj._meta.app_label, obj._meta.model_name)
        link = reverse(view_name, args=[obj.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
        return format_html(html)

    def make_books_available(modeladmin, request, queryset):
        queryset.update(is_available=True)

    make_books_available.short_description = "Mark selected books as available"

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
        book.is_available = True
        book.save()
        return redirect(reverse("admin:book_book_changelist"))


class BookAdmin2(admin.ModelAdmin):
    list_display = ('id', 'name_colored', 'thumbnail', 'author', 'published_date', 'is_available', 'cover', 'thumbnail')
    search_fields = ('name',)
    autocomplete_fields = ['author']
    list_filter = ('is_available',)
    date_hierarchy = 'published_date'

    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('created_at', 'updated_at')

    # formfield_overrides = {
    #     JSONField: {
    #         'widget': JSONEditorWidget
    #     },
    # }

    def name_colored(self, obj):
        if obj.is_available:
            color_code = '00FF00'
        else:
            color_code = 'FF0000'
        html = '<span style="color: #{};">{}</span>'.format(color_code, obj.name)
        return format_html(html)

    name_colored.admin_order_field = 'name'
    name_colored.short_description = 'name'

    def thumbnail(self, obj):
        width, height = 100, 140
        if not obj.cover:
            return
        print(obj.cover.url)
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.cover.url,
            width=width,
            height=height,
        ))

        # def get_queryset(self, request):
        #     qs = super().get_queryset(request)
        #     qs = qs.only('id', 'name')
        #     return qs


class CenturyFilter(admin.SimpleListFilter):
    title = 'century'
    parameter_name = 'published_date'

    def lookups(self, request, model_admin):
        return (
            (21, '21st century'),
            (20, '20th century'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        start = (int(value) - 1) * 100
        end = start + 99
        return queryset.filter(published_date__year__gte=start, published_date__year__lte=end)


class InputFilter(admin.SimpleListFilter):
    template = 'admin_input_filter.html'

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class PublishedYearFilter2(InputFilter):
    title = 'published year'
    parameter_name = 'published_date'

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(published_date__year=value)


class PublishedYearFilter(admin.SimpleListFilter):
    title = 'published year'
    parameter_name = 'published_date'
    template = 'admin_input_filter.html'

    def lookups(self, request, model_admin):
        return ((None, None),)

    def choices(self, changelist):
        query_params = changelist.get_filters_params()
        query_params.pop(self.parameter_name, None)
        all_choice = next(super().choices(changelist))
        all_choice['query_params'] = query_params
        yield all_choice

    def queryset(self, request, queryset):
        self.qvalue = self.value()
        if self.qvalue:
            return queryset.filter(published_date__year=self.qvalue)


class BookAdminFilter(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'published_date', 'is_available', 'name', 'author',)
    # list_filter = ('is_available', CenturyFilter, PublishedYearFilter)


    list_filter = ('is_available', )
    list_filter = (CenturyFilter, )
    list_filter = (PublishedYearFilter, 'is_available',)
    search_fields = ('name',)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'active', 'active', 'active', 'name', 'name')


admin.site.register(Author, AuthorAdmin)


# admin.site.register(Author)




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

# database = 'legacy_db'


def load_dynamic_admin(database):
    models_file = get_models(database)
    spec = importlib.util.spec_from_file_location("trash.models", models_file)
    # spec = importlib.util.spec_from_file_location("my_new_app.models", models_file)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)


# load_dynamic_admin(database)


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
    autocomplete_fields = ['book']

    # list_display = ('book', 'book__author')
    # book_author = get_related_field('book__author')


class BookProxyAdmin(admin.ModelAdmin):
    list_display = ('name',)


class BookAdAdminFilter(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('id', 'name', 'author', 'published_date', 'is_available', 'name', 'author',)
    advanced_filter_fields = ('name', 'published_date', 'author', 'is_available')
    date_hierarchy = 'published_date'


# admin_site.register(BestSeller, BestSellerAdmin)
admin_site.register(BestSeller)
admin_site.register(BookProxy, BookProxyAdmin)

# admin.site.register(Book)
# admin.site.register(Book, BookAdmin)
# admin.site.register(Book, BookAdmin2)
# admin.site.register(Book, BookAdminFilter)
admin.site.register(Book, BookAdAdminFilter)

# admin.site.register(BestSeller)
admin.site.register(BestSeller, BestSellerAdmin)
