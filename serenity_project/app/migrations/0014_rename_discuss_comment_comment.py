# Generated by Django 3.2.16 on 2022-11-08 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_name_email_comment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="discuss",
            new_name="comment",
        ),
    ]
