# Generated by Django 3.2.9 on 2022-05-11 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0001_initial'),
        ('question', '0001_initial'),
        ('category', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last Name')),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Middle Name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email')),
                ('bio', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Biography')),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], max_length=10, null=True, verbose_name='Gender')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date Of Birth')),
                ('state_of_residence', models.CharField(blank=True, max_length=100, null=True, verbose_name='state Of Residence')),
                ('state_of_origin', models.CharField(blank=True, max_length=100, null=True, verbose_name='State Of Origin')),
                ('nationality', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nationlity')),
                ('language1', models.CharField(blank=True, max_length=100, null=True, verbose_name='First Language')),
                ('language2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Second Language')),
                ('coins', models.DecimalField(decimal_places=2, default=20.0, max_digits=200)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(blank=True, max_length=32, null=True)),
                ('refercount', models.PositiveIntegerField(default=0)),
                ('views', models.PositiveIntegerField(default=0)),
                ('quizAvgScore', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('questionAvgScore', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('quizAttempts', models.IntegerField(default=0)),
                ('questionAttempts', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('quizzes', models.IntegerField(default=0)),
                ('categories', models.ManyToManyField(blank=True, related_name='profileCategories', to='category.Category')),
                ('favoriteQuizzes', models.ManyToManyField(blank=True, related_name='favoriteQuizzes', to='quiz.Quiz')),
                ('fourChoicesQuestionsMissed', models.ManyToManyField(blank=True, related_name='fourChoicesQuestionsMissed', to='question.FourChoicesQuestion')),
                ('fourChoicesQuestionsTaken', models.ManyToManyField(blank=True, related_name='fourChoicesQuestionsTaken', to='question.FourChoicesQuestion')),
                ('quizTaken', models.ManyToManyField(blank=True, related_name='profileQuizTaken', to='quiz.Quiz')),
                ('trueOrFalseQuestionsMissed', models.ManyToManyField(blank=True, related_name='trueOrFalseQuestionsMissed', to='question.TrueOrFalseQuestion')),
                ('trueOrFalseQuestionsTaken', models.ManyToManyField(blank=True, related_name='trueOrFalseQuestionsTaken', to='question.TrueOrFalseQuestion')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Streak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('currentDate', models.DateField(auto_now=True, null=True)),
                ('length', models.PositiveIntegerField(default=0)),
                ('question', models.PositiveIntegerField(default=0)),
                ('freeze', models.BooleanField(default=False)),
                ('profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('clicks', models.PositiveIntegerField(default=0)),
                ('date_updated', models.DateTimeField(blank=True, null=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.TextField(blank=True, max_length=1000, null=True, verbose_name='What do you like most about this app?')),
                ('dislike', models.TextField(blank=True, max_length=1000, null=True, verbose_name="What don't you like about this app?")),
                ('modifier', models.TextField(blank=True, max_length=1000, null=True, verbose_name='What do you want us to add to this app?')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
