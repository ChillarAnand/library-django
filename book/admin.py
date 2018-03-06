from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Author, Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'delete', )
    list_display = ('name', 'author_link', )
    list_display = ('name', 'author_link', 'name', 'name')
    list_display = ('name', 'author', 'name', 'name')

    list_display_links = ('name', 'author',)

    def author_link(self, book):
        link = reverse("admin:book_author_change", args=[book.author.id])
        return u'<a href="%s">%s</a>' % (link, book.author.name)
    author_link.allow_tags = True
    author_link.short_description = 'Author'

    def delete(self, book):
        link = reverse("admin:book_book_delete", args=[book.pk])
        button = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'
        return button.format(link)
    delete.allow_tags = True
    delete.short_description = 'Delete book'


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
