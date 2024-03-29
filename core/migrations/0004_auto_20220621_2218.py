# Generated by Django 3.2.9 on 2022-06-21 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
        ('quiz', '0002_auto_20220621_2156'),
        ('core', '0003_auto_20220621_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fourChoicesQuestionsMissed',
            field=models.ManyToManyField(blank=True, related_name='fourChoicesQuestionsMissed', to='question.FourChoicesQuestion'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fourChoicesQuestionsTaken',
            field=models.ManyToManyField(blank=True, related_name='fourChoicesQuestionsTaken', to='question.FourChoicesQuestion'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fourChoicesQuestionsWareHouse',
            field=models.ManyToManyField(blank=True, related_name='fourChoicesQuestionsWareHouse', to='question.FourChoicesQuestion'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='quizTaken',
            field=models.ManyToManyField(blank=True, related_name='profileQuizTaken', to='quiz.Quiz'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='quizWareHouse',
            field=models.ManyToManyField(blank=True, related_name='profileQuizWareHouse', to='quiz.Quiz'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='trueOrFalseQuestionsMissed',
            field=models.ManyToManyField(blank=True, related_name='trueOrFalseQuestionsMissed', to='question.TrueOrFalseQuestion'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='trueOrFalseQuestionsTaken',
            field=models.ManyToManyField(blank=True, related_name='trueOrFalseQuestionsTaken', to='question.TrueOrFalseQuestion'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='trueOrFalseQuestionsWareHouse',
            field=models.ManyToManyField(blank=True, related_name='trueOrFalseQuestionsWareHouse', to='question.TrueOrFalseQuestion'),
        ),
    ]
