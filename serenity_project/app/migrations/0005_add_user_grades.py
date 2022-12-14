# Generated by Django 3.2.16 on 2022-10-31 14:24

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("app", "0004_alter_scoretable_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="scoretable",
            name="gradeCount",
            field=models.FloatField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="scoretable",
            name="userAvg",
            field=models.FloatField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="scoretable",
            name="userGrace",
            field=models.FloatField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
