from django.contrib import admin
from .models import Profile, RecruiterProfile, Vacante, Postulacion

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'phone')
    search_fields = ('user__username', 'bio', 'location')

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'phone')
    search_fields = ('user__username', 'company', 'position')

@admin.register(Vacante)
class VacanteAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'employment_type', 'date')
    list_filter = ('employment_type', 'date')
    search_fields = ('title', 'company', 'location', 'description')

@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'vacante', 'estado', 'fecha_postulacion')
    list_filter = ('estado', 'fecha_postulacion')
    search_fields = ('usuario__username', 'vacante__title', 'vacante__company')
    readonly_fields = ('fecha_postulacion',)
