from django.test import TestCase
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

TestCase
TransactionTestCase


class BookTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        print('BookTestCase setUpClass')
        return
        super(TransactionTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        return
        super(TransactionTestCase, cls).tearDownClass()

    def setUp(self) -> None:
        # super().setUp()
        self.client = APIClient()

    def test_post_books(self):
        url = reverse('books-list')
        data = {'name': 'test book', 'slug': 'test-book'}
        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        response = self.client.get(url)
        book = response.json()[0]

        assert book['name'] == data['name']


