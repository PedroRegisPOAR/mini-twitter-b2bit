# Generated by Django 5.1.2 on 2024-10-22 02:15

import django.contrib.auth.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=20, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator], verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='endereço de email')),
                ('name', models.CharField(max_length=200, verbose_name='nome do usuário')),
                ('password', models.CharField(max_length=150, verbose_name='senha do usuário')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'ordering': ['-created_at'],
            },
        ),
    ]
