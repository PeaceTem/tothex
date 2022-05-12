# Generated by Django 3.2.9 on 2022-05-11 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('relevance', models.IntegerField(default=0)),
                ('number_of_quizzes', models.PositiveIntegerField(default=0)),
                ('number_of_questions', models.PositiveIntegerField(default=0)),
                ('quiz_number_of_times_taken', models.PositiveIntegerField(default=0)),
                ('question_number_of_times_taken', models.PositiveIntegerField(default=0)),
                ('date_registered', models.DateTimeField(auto_now_add=True)),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
    ]
