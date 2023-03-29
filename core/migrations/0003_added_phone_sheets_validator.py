# Generated by Django 4.1.7 on 2023-03-29 08:56

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_reader_added_is_active_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='sheets',
            field=models.PositiveSmallIntegerField(validators=[core.validators.BookNegativeSheetsValidator()], verbose_name='Кол-во страниц'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='phone',
            field=models.CharField(max_length=20, validators=[core.validators.RussianPhoneValidator()], verbose_name='№ телефона'),
        ),
    ]