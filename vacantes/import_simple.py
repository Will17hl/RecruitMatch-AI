import os
import sys
import django

# Agregar el directorio del proyecto al path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recruitmatch.settings')
django.setup()

import csv
from django.contrib.auth.models import User
from vacantes.models import Vacante
from django.utils import timezone

# Crear usuario por defecto
user, _ = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@example.com',
        'is_staff': True,
        'is_superuser': True
    }
)
user.set_password('admin123')
user.save()

# Leer el archivo CSV y crear las vacantes
with open('vacantes_1000_colombia.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        try:
            Vacante.objects.create(
                title=row['title'],
                company=row.get('company', 'Empresa no especificada'),
                location=row.get('location', 'Ubicación no especificada'),
                description=row.get('description', 'Sin descripción'),
                requirements=row.get('area', 'Sin requisitos específicos'),
                salary=row.get('salary', 'Salario a convenir'),
                date=timezone.now(),
                user=user
            )
            print(f'Vacante creada: {row["title"]}')
        except Exception as e:
            print(f'Error al crear vacante: {e}') 