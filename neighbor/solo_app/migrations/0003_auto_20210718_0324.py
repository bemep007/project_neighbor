# Generated by Django 2.2 on 2021-07-18 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solo_app', '0002_invited'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='author',
            new_name='title',
        ),
    ]