from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from core.models import Book, Author, Reader
from core.permissions import IsReaderOwner
from core.serializers import BookListRetrieveSerializer, BookCreateUpdateDestroySerializer, \
    AuthorListRetrieveSerializer, AuthorCreateUpdateDestroySerializer, \
    ReaderListRetrieveSerializer, ReaderCreateUpdateDestroySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    http_method_names = ["get", "post", "put", 'delete']

    serializer_classes = {
        'create': BookCreateUpdateDestroySerializer,
        'list': BookListRetrieveSerializer,
        'retrieve': BookListRetrieveSerializer,
        'update': BookCreateUpdateDestroySerializer,
        'destroy': BookCreateUpdateDestroySerializer,
    }

    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    http_method_names = ["get", "post", "put", 'delete']

    serializer_classes = {
        'create': AuthorCreateUpdateDestroySerializer,
        'list': AuthorListRetrieveSerializer,
        'retrieve': AuthorListRetrieveSerializer,
        'update': AuthorCreateUpdateDestroySerializer,
        'destroy': AuthorCreateUpdateDestroySerializer,
    }

    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    http_method_names = ["get", "post", "put", 'delete']

    serializer_classes = {
        'create': ReaderCreateUpdateDestroySerializer,
        'list': ReaderListRetrieveSerializer,
        'retrieve': ReaderListRetrieveSerializer,
        'update': ReaderCreateUpdateDestroySerializer,
        'destroy': ReaderCreateUpdateDestroySerializer,
    }

    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsReaderOwner | IsAdminUser],
        'create': [AllowAny],
        'update': [IsReaderOwner | IsAdminUser],
        'destroy': [IsReaderOwner | IsAdminUser],
    }


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)
