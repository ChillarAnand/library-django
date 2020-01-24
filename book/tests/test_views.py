from django.test import TestCase
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from book.models import Book


class TransactionMixin:
    @classmethod
    def _enter_atomics(cls):
        return {}

    @classmethod
    def _rollback_atomics(cls, atomics):
        return {}


class TransactionMixin2:
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls).tearDownClass()

    def _fixture_setup(self):
        return super(TestCase, self)._fixture_setup()

    def _fixture_teardown(self):
        return super(TestCase, self)._fixture_teardown()



class LibraryTestCase(TestCase):
    pass


class LibraryUserTestCase(LibraryTestCase):
    pass


TestCase
TransactionTestCase


class LibraryPaidUserTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_post_books(self):
        # list(Book.objects.select_for_update().filter())

        url = reverse('books-list')
        data = {'name': 'test book', 'slug': 'test-book'}
        Book.objects.filter(name=data['name']).delete()
        Book.objects.create(name=data['name'], slug=data['slug'])
        # response = self.client.post(url, data=data)
        # assert response.status_code == status.HTTP_201_CREATED
        list(Book.objects.select_for_update().all())

        response = self.client.get(url)
        book = response.json()[0]

        assert book['name'] == data['name']
