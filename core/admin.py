from django.contrib import admin
from django.db import transaction
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.models import Author, Book, Reader


class CustomBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_author', 'short_description', 'sheets', 'quantity')
    actions = ['set_zero_quantity']

    def short_description(self, obj):
        if len(obj.description) > 100:
            return f"{obj.description[:100]}..."
        return obj.description
    short_description.short_description = "Описание"

    def link_to_author(self, obj):
        url = reverse("admin:core_author_change", args=[obj.author.id])
        link = f'<a href="{url}">{obj.author}</a>'

        return mark_safe(link)
    link_to_author.short_description = 'Автор'

    @admin.action(description='Установить 0 наличие')
    def set_zero_quantity(self, request, queryset):
        queryset.update(quantity=0)


class CustomAuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'photo')


class CustomReaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'is_active')
    list_filter = ('is_active', )
    actions = ['set_opposite_activity', 'rm_active_books']

    @admin.action(description='Сменить статус')
    def set_opposite_activity(self, request, queryset):
        for reader in queryset:
            reader.is_active = not reader.is_active
            reader.save()

    @admin.action(description='Удалить активные книги')
    def rm_active_books(self, request, queryset):
        queryset = queryset.prefetch_related('active_books')
        books = [book for reader in queryset for book in reader.active_books.all()]
        with transaction.atomic():
            for book in books:
                book.quantity += 1
                book.save()
            [reader.active_books.clear() for reader in queryset]


#registration
admin.site.register(Author, CustomAuthorAdmin)
admin.site.register(Book, CustomBookAdmin)
admin.site.register(Reader, CustomReaderAdmin)

