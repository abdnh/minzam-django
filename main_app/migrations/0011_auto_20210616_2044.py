# Generated by Django 3.2.4 on 2021-06-16 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20210616_0219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['due_date', 'priority']},
        ),
        migrations.AddField(
            model_name='task',
            name='notified',
            field=models.BooleanField(default=False, verbose_name='تم التنبيه'),
            preserve_default=False,
        ),
    ]
