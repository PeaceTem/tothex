# Generated by Django 3.2.9 on 2022-07-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20220728_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='total_coins',
            field=models.FloatField(default=0),
        ),
    ]