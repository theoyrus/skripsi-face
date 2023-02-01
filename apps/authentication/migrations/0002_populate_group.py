# Generated by Django 3.2.16 on 2023-01-17 21:00

from django.db import migrations
from django.core.management import call_command


def forwards_func(apps, schema_editor):
    print("forwards")
    call_command("loaddata", "data.json", verbosity=2)


def reverse_func(apps, schema_editor):
    print("reverse")


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [migrations.RunPython(forwards_func, reverse_func, elidable=False)]
