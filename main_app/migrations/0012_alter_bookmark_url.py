# Generated by Django 3.2.4 on 2021-06-17 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_auto_20210616_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='url',
            field=models.URLField(verbose_name='رابط'),
        ),
    ]
