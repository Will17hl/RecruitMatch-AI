from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse

class Vacante(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Tiempo completo'),
        ('part_time', 'Medio tiempo'),
        ('contract', 'Contrato'),
        ('temporary', 'Temporal'),
        ('internship', 'Prácticas'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título", default="Sin título")
    description = models.TextField(verbose_name="Descripción", default="Sin descripción")
    company = models.CharField(max_length=100, verbose_name="Empresa", default="Empresa no especificada")
    location = models.CharField(max_length=100, verbose_name="Ubicación", default="Ubicación no especificada")
    requirements = models.TextField(verbose_name="Requisitos", default="Sin requisitos especificados")
    salary = models.CharField(max_length=100, verbose_name="Salario", default="Salario no especificado", blank=True, null=True)
    website = models.URLField(verbose_name="Sitio web", blank=True, null=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, verbose_name="Tipo de empleo", default='full_time')
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    postulantes = models.ManyToManyField(User, through='Postulacion', related_name='vacantes_postuladas')
    favoritos = models.ManyToManyField(User, related_name='vacantes_favoritas', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vacante_detail', args=[str(self.id)])

class Postulacion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente por confirmar'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'vacante')

    def __str__(self):
        return f"{self.usuario.username} - {self.vacante.title} - {self.estado}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    rol = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='profiles/images/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    company_logo = models.ImageField(upload_to='recruiters/logos/', null=True, blank=True)
    company_website = models.URLField(blank=True)
    company_location = models.CharField(max_length=200)
    company_size = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.user.username}"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.company}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()