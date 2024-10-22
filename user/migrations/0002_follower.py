# Generated by Django 5.1.2 on 2024-10-22 02:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='followings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Seguidor',
                'verbose_name_plural': 'Seguidores',
                'ordering': ['-created_at'],
                'unique_together': {('following', 'follower')},
            },
        ),
    ]
