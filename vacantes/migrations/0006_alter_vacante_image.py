# Generated by Django 5.1.5 on 2025-04-01 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0005_alter_vacante_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacante',
            name='image',
            field=models.ImageField(blank=True, default='vacante/images/default.jpeg', null=True, upload_to='vacante/images/'),
        ),
    ]
