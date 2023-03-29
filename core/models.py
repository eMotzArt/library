from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models.signals import m2m_changed

from core.validators import RussianPhoneValidator, BookNegativeSheetsValidator


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    edited_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        abstract = True


class Author(BaseModel):
    def get_file_name(self, file_name):
        return f'author_photos/{self.name}_{self.surname}_{file_name}'

    name = models.CharField(max_length=32, verbose_name="Имя")
    surname = models.CharField(max_length=64, verbose_name="Фамилия")
    photo = models.ImageField(null=True, blank=True, upload_to=get_file_name, verbose_name="Фотография")


    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Book(BaseModel):
    title = models.CharField(max_length=64, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', verbose_name="Автор")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    sheets = models.PositiveSmallIntegerField(validators=[BookNegativeSheetsValidator()], verbose_name="Кол-во страниц")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Кол-во шт.")

    def __str__(self):
        return f"{self.author.name[0].title()}.{self.author.surname} - {self.title}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Reader(BaseModel):
    name = models.CharField(max_length=32, verbose_name="Имя")
    surname = models.CharField(max_length=64, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, validators=[RussianPhoneValidator()], verbose_name="№ телефона")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    active_books = models.ManyToManyField(Book, blank=True, verbose_name="Взятые книги")

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"


# signals
def reader_active_books_changed(sender, **kwargs):
    action = kwargs['action']

    if action == 'post_remove':
        books = [book for book in Book.objects.filter(pk__in=kwargs['pk_set']).all()]
        with transaction.atomic():
            for book in books:
                book.quantity += 1
                book.save()

    if action == 'pre_add':
        non_quantity_books = [book_id for book_id in kwargs['pk_set'] if not Book.objects.get(pk=book_id).quantity]
        if non_quantity_books:
            raise ValidationError(f"You can't assign book with 0 quantity. (books ids: {non_quantity_books}")

        if kwargs['instance'].active_books.count() + len(kwargs['pk_set']) > 3:
            raise ValidationError("You can't assign more than three books to reader")

    if action == 'post_add':
        books = [book for book in Book.objects.filter(pk__in=kwargs['pk_set']).all()]
        for book in books:
            book.quantity -= 1
            book.save()

m2m_changed.connect(reader_active_books_changed, sender=Reader.active_books.through)