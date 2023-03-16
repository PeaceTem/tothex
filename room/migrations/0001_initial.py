# Generated by Django 3.2.9 on 2022-10-03 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('q', '0010_auto_20220925_2349'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0015_auto_20220920_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('fourChoicesQuestions', models.ManyToManyField(blank=True, related_name='rooms', to='question.FourChoicesQuestion')),
                ('members', models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL)),
                ('questions', models.ManyToManyField(blank=True, related_name='rooms', to='q.Q')),
                ('trueOrFalseQuestions', models.ManyToManyField(blank=True, related_name='rooms', to='question.TrueOrFalseQuestion')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement', models.CharField(blank=True, max_length=1000, null=True)),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='announcement', to='room.studyroom')),
            ],
        ),
    ]