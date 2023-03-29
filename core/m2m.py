from django.core.exceptions import ValidationError


def reader_active_books_changed(sender, **kwargs):
    from core.models import Book
    action = kwargs['action']

    if action == 'post_remove':
        for book in Book.objects.filter(pk__in=kwargs['pk_set']):
            book.quantity += 1
            book.save()

    elif action == 'pre_add':
        non_quantity_books = [book_id for book_id in kwargs['pk_set'] if not Book.objects.get(pk=book_id).quantity]
        if non_quantity_books:
            raise ValidationError(f"You can't assign book with 0 quantity. (books ids: {non_quantity_books}")

        if kwargs['instance'].active_books.count() + len(kwargs['pk_set']) > 3:
            raise ValidationError("You can't assign more than three books to reader")

    elif action == 'post_add':
        books = [book for book in Book.objects.filter(pk__in=kwargs['pk_set']).all()]
        for book in books:
            book.quantity -= 1
            book.save()
