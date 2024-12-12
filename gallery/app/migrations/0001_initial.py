# Generated by Django 5.1.2 on 2024-12-12 10:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.TextField()),
                ('name', models.TextField()),
                ('file', models.FileField(upload_to='')),
                ('images', models.BooleanField(default=False)),
                ('video', models.BooleanField(default=False)),
                ('audio', models.BooleanField(default=False)),
                ('others', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.gallery')),
            ],
        ),
    ]
