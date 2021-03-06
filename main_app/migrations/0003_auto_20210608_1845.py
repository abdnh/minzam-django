# Generated by Django 3.2.4 on 2021-06-08 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210608_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(to='main_app.Tag'),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
