# Generated by Django 3.2 on 2025-02-21 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='Рейтинг'),
        ),
    ]
