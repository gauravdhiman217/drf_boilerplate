# Generated by Django 5.1.1 on 2024-10-09 18:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_alter_user_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("M", "Male"), ("F", "FEMALE"), ("O", "Other")],
                max_length=1,
                null=True,
            ),
        ),
    ]
