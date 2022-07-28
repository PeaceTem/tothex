# Generated by Django 3.2.9 on 2022-07-28 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20220728_0053'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0003_alter_fourchoicesquestion_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='fourchoicesquestion',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fourChoicesQuestions', to='quiz.quiz'),
        ),
        migrations.AddField(
            model_name='trueorfalsequestion',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trueOrFalseQuestions', to='quiz.quiz'),
        ),
        migrations.AlterField(
            model_name='fourchoicesquestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fourchoicesquestions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trueorfalsequestion',
            name='correct',
            field=models.CharField(choices=[('answer1', 'True'), ('answer2', 'False')], max_length=100, verbose_name='Correct Option'),
        ),
        migrations.AlterField(
            model_name='trueorfalsequestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trueOrFalseQuestions', to=settings.AUTH_USER_MODEL),
        ),
    ]
