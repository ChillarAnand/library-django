from django.views import generic

from .models import Book


class BookListView(generic.ListView):
    model = Book
    # template_name = 'foo.html'
    # template_engine = 'jinja2'
