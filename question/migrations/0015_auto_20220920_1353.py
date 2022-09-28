# Generated by Django 3.2.9 on 2022-09-20 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0014_auto_20220913_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='fourchoicesquestion',
            name='question_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/fourChoicesQuestion/'),
        ),
        migrations.AddField(
            model_name='fourchoicesquestion',
            name='solution_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/fourChoicesQuestion/solution/'),
        ),
        migrations.AddField(
            model_name='trueorfalsequestion',
            name='question_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/trueOrFalseQuestion/'),
        ),
        migrations.AddField(
            model_name='trueorfalsequestion',
            name='solution_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/trueOrFalseQuestion/solution/'),
        ),
        migrations.AlterField(
            model_name='fourchoicesquestion',
            name='standalone',
            field=models.BooleanField(default=True, verbose_name='Make this question public'),
        ),
        migrations.AlterField(
            model_name='trueorfalsequestion',
            name='standalone',
            field=models.BooleanField(default=True, verbose_name='Make this question public'),
        ),
    ]