# Generated by Django 3.2 on 2025-02-23 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_title_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
