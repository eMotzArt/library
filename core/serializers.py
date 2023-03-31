from rest_framework import serializers

from core.models import Book, Author, Reader


class BookListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookCreateUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'edited_at']


class AuthorListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorCreateUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'edited_at']


class ReaderListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'


class ReaderCreateUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'edited_at']
