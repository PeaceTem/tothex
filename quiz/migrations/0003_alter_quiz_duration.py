# Generated by Django 3.2.9 on 2022-07-27 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20220621_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='duration',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
