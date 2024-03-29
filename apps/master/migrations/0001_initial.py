# Generated by Django 3.2.17 on 2023-02-16 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_pref', to=settings.AUTH_USER_MODEL)),
                ('pref', models.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'preferensi',
                'db_table': 'preferensi',
            },
        ),
    ]
