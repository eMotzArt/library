from django.contrib import admin
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

from core.models import Author, Book, Reader

# Register your models here.

def active_books_changed(sender, **kwargs):
    if kwargs['action'] == 'pre_add':

        non_quantity_books = [book_id for book_id in kwargs['pk_set'] if not Book.objects.get(pk=book_id).count]
        if non_quantity_books:
            raise ValidationError(f"You can't assign book with 0 quantity. (books ids: {non_quantity_books}")

        if kwargs['instance'].active_books.count() + len(kwargs['pk_set']) > 3:
            raise ValidationError("You can't assign more than three books to reader")

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Reader)

m2m_changed.connect(active_books_changed, sender=Reader.active_books.through)