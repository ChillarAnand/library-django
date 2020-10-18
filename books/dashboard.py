from controlcenter import Dashboard
from controlcenter import widgets
from django.db import connection
from django.db.models import Count

from books.models import Book


class BookList(widgets.ItemList):
    model = Book
    list_display = ('name', 'published_date')
    limit_to = 20


class BookSeriesChart(widgets.TimeSeriesChart):
    def series(self):
        x = [
            [{'x': book.created_at.timestamp(), 'y': book.name} for book in Book.objects.all()],
        ]
        # print(x)
        return x


class BookLineChart(widgets.LineChart):
    def series(self):
        # qs = Book.objects.values('published_date').annotate(count=Count('published_date'))
        truncate_year = connection.ops.date_trunc_sql('year', 'published_date')
        qs = Book.objects.extra({'year': truncate_year})
        qs = qs.values('year').annotate(count=Count('pk'))

        x = [
            [{'x': book['year'], 'y': book['count']} for book in qs],
        ]
        print(x)
        return x

    def labels(self):
        return self.series

    # def legend(self):
    #     # Displays labels in legend
    #     return [x for x, y in self.series()[0][0]]


class BookBarChart(widgets.TimeSeriesChart):
    values_list = ('name', 'published_date')
    list_display = ('name', 'published_date')
    model = Book
    limit_to = None


class BookDashboard(Dashboard):
    widgets = (
        BookList,
        BookLineChart,
        BookSeriesChart,
        BookBarChart,
    )
