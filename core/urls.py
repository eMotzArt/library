from django.urls import path, include
from rest_framework.routers import SimpleRouter

from core import views

book_router = SimpleRouter()
book_router.register(r'books', views.BookViewSet, basename="books")

author_router = SimpleRouter()
author_router.register(r'authors', views.AuthorViewSet, basename="authors")

reader_router = SimpleRouter()
reader_router.register(r'readers', views.ReaderViewSet, basename="readers")

urlpatterns = [
    path('', include(book_router.urls)),
    path('', include(author_router.urls)),
    path('', include(reader_router.urls)),
]
