# Generated by Django 3.2.16 on 2022-11-01 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_auto_20221101_1516"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Discussion",
            new_name="Comment",
        ),
    ]
