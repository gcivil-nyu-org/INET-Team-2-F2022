# Generated by Django 3.2.16 on 2022-11-01 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ("app", "0011_forumpost_zipcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forumpost",
            name="zipcode",
            field=models.ForeignKey(
                blank=True,
                default=1,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.scoretable",
            ),
        ),
    ]
