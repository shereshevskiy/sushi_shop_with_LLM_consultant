# Generated by Django 5.0.3 on 2024-04-03 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neuro_assistant', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='chunk',
            options={'verbose_name': 'Чанк', 'verbose_name_plural': 'Чанки'},
        ),
    ]
