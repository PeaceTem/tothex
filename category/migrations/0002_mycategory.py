# Generated by Django 3.2.9 on 2022-10-21 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_categories', to='category.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myCategories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]