# Generated by Django 5.1.1 on 2024-10-06 11:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="updated_on",
            new_name="updated_at",
        ),
    ]
