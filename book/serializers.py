from rest_framework.serializers import ModelSerializer

from book.models import Author
from book.models import Book


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
