# Generated by Django 3.2.9 on 2022-07-23 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_favoriteusers_profile_favoriteuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_question_date',
            field=models.DateTimeField(null=True),
        ),
    ]