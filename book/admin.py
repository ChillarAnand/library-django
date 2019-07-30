from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html

try:
    from django.urls import reverse
except ImportError:
    # django < 2
    from django.core.urlresolvers import reverse

from . import models
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


admin.site.register(models.Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'active')


admin.site.register(models.Author, AuthorAdmin)


class HouseAdmin(admin.ModelAdmin):
    def url_for_result(self, house):
        html_string = format_html(u'<a href="/admin/crm/house/{}/change/">{}', house.id, house.id)
        return html_string

    list_display = ('id', 'url_for_result', 'id', )


admin.site.register(House, HouseAdmin)
