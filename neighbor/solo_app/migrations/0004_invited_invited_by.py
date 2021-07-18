# Generated by Django 2.2 on 2021-07-18 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solo_app', '0003_auto_20210718_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='invited',
            name='invited_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='has_invited_neighbor', to='solo_app.User'),
            preserve_default=False,
        ),
    ]