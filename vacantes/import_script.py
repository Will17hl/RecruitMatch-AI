import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recruitmatch.settings')
django.setup()

import csv
from django.contrib.auth.models import User
from vacantes.models import Vacante
from django.utils import timezone
from datetime import datetime

def import_vacantes():
    # Crear usuario por defecto
    user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'password': 'admin123'}
    )

    # Leer el archivo CSV y crear las vacantes
    with open('vacantes_1000_colombia.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            try:
                # Convertir la fecha del formato del CSV al formato de Django
                fecha = datetime.strptime(row['date'], '%Y-%m-%d')
                
                Vacante.objects.create(
                    title=row['title'],
                    company=row['company'],
                    location=row['location'],
                    description=row['description'],
                    requirements=row.get('area', 'Sin requisitos específicos'),
                    salary='Salario a convenir',
                    date=fecha,
                    user=user
                )
                print(f'Vacante creada: {row["title"]}')
            except Exception as e:
                print(f'Error al crear vacante: {e}')

if __name__ == '__main__':
    import_vacantes() 