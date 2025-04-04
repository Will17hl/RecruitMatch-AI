# Generated by Django 5.1.5 on 2025-04-04 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cc', models.CharField(max_length=20, unique=True)),
                ('estudios', models.CharField(max_length=200)),
                ('tipo', models.CharField(choices=[('influencer', 'Influencer'), ('candidato', 'Candidato')], max_length=10)),
                ('correo', models.EmailField(max_length=254)),
            ],
        ),
    ]
