from django.core.management.base import BaseCommand
import csv
import os
from django.contrib.auth.models import User
from vacantes.models import Vacante
from django.utils import timezone

class Command(BaseCommand):
    help = 'Importa vacantes desde un archivo CSV'

    def handle(self, *args, **options):
        # Crear usuario por defecto si no existe
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Usuario admin creado exitosamente'))

        # Verificar si el archivo existe
        csv_path = 'vacantes_1000_colombia.csv'
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo {csv_path}'))
            return

        # Contadores para estadísticas
        total = 0
        creadas = 0
        errores = 0

        # Leer el archivo CSV y crear las vacantes
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                total += 1
                try:
                    vacante = Vacante.objects.create(
                        title=row['title'],
                        company=row.get('company', 'Empresa no especificada'),
                        location=row.get('location', 'Ubicación no especificada'),
                        description=row.get('description', 'Sin descripción'),
                        requirements=row.get('area', 'Sin requisitos específicos'),
                        salary=row.get('salary', 'Salario a convenir'),
                        date=timezone.now(),
                        user=user
                    )
                    creadas += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Vacante creada: {vacante.title}'))
                except Exception as e:
                    errores += 1
                    self.stdout.write(self.style.ERROR(f'✗ Error al crear vacante: {row.get("title", "Sin título")}'))
                    self.stdout.write(self.style.ERROR(f'  Error: {str(e)}'))

        # Mostrar estadísticas finales
        self.stdout.write(self.style.SUCCESS('\nResumen de importación:'))
        self.stdout.write(self.style.SUCCESS(f'Total de registros procesados: {total}'))
        self.stdout.write(self.style.SUCCESS(f'Vacantes creadas exitosamente: {creadas}'))
        self.stdout.write(self.style.ERROR(f'Errores encontrados: {errores}')) 