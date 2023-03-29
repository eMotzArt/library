from django.apps import AppConfig
from django.db.models.signals import m2m_changed
from core.m2m import reader_active_books_changed


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        Reader = self.get_model("Reader")

        m2m_changed.connect(reader_active_books_changed, sender=Reader.active_books.through)
