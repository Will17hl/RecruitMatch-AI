# Generated by Django 5.1.5 on 2025-03-11 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacante',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
