# Generated by Django 5.0.6 on 2024-06-16 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mining", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertisement",
            name="publication_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="advertisement",
            name="submission_deadline",
            field=models.DateField(blank=True, null=True),
        ),
    ]