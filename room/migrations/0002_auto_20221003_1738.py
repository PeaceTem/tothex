# Generated by Django 3.2.9 on 2022-10-03 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('q', '0010_auto_20220925_2349'),
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyroom',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studyroom',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='q.Q'),
        ),
    ]
