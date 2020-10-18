import concurrent
import time

from django import forms
from django.conf import settings
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from books.models import Author
from books.models import Book
from books.serializers import AuthorSerializer
from books.serializers import BookSerializer


# from silk.profiling.profiler import silk_profile


class AuthorViewSet(ViewSet):

    def list(self, request):
        queryset = Author.objects.all()
        serializer = AuthorSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Author.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = AuthorSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response(status=404)
        serializer = AuthorSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class BookViewSet(ViewSet):

    @staticmethod
    def get_books(*args):
        # queryset = Book.objects.select_for_update().all()
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        response = serializer.data
        return response

    def list(self, request):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(BookViewSet.get_books, ())
            return_value = future.result()

        # Book.objects.select_for_update().first()
        # return_value = BookViewSet.get_books()

        try:
            params = request.GET
            delay = request.GET.get('delay')
            if delay:
                time.sleep(int(delay))
        except:
            pass
        return Response(return_value)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        time.sleep(2)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Book.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        time.sleep(3)
        try:
            item = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=404)
        serializer = BookSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


def test(request):
    return Response()


def comp(request):
    x = []
    for i in range(1000_000_0):
        x.append(2)
    return JsonResponse({'data': 'slow_response'})


def sleep(request):
    time.sleep(4)
    return JsonResponse({'data': 'slow_response'})


error = test
email_book = test
home = test



def hello(request):
    return JsonResponse({'data': 'hello'})


class BookForm(forms.Form):
    name = forms.CharField()


def book_form(request):
    template = 'books.html'

    if request.method == 'GET':
        form = BookForm()
        context = {'form': form}
        return render(request, template, context)

    # POST Workflow
    form = BookForm(data=request.POST)
    if not form.is_valid():
        return render(request, template, context)

    # books = Book.objects.create()
    return HttpResponseRedirect(reverse('hello'))

def black_hole(request, *args, **kwargs):
    path = request.path
    start = now()
    try:
        params = request.GET
        delay = request.GET.get('delay')
        if delay:
            time.sleep(int(delay))
    except:
        pass

    end = now()
    delta = end-start
    data = {
        'path': path,
        'params': params,
        'duration': delta.seconds,
    }
    return JsonResponse(data)


def home(request):
    context = {
        'version': settings.VERSION,
        'urls': {
            'error': '/error',
            'admin': '/admin',
            'slow': '/books/books/?delay=4',
        }
    }
    return render(request, template_name='home.html', context=context)
