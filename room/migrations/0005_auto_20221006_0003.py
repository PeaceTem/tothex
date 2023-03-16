# Generated by Django 3.2.9 on 2022-10-05 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_auto_20221004_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomfourchoicesquestion',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fourChoicesQuestions', to='room.studyroom'),
        ),
        migrations.AddField(
            model_name='roomquestion',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='room.studyroom'),
        ),
        migrations.AddField(
            model_name='roomquiz',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='room.studyroom'),
        ),
        migrations.AddField(
            model_name='roomtrueorfalsequestion',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trueOrFalseQuestions', to='room.studyroom'),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='room.studyroom'),
        ),
    ]