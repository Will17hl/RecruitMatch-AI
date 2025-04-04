from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('recruiter-profile/', views.recruiter_profile, name='recruiter_profile'),
    path('vacantes/', views.vacantes_list, name='vacantes_list'),
    path('vacante/<int:vacante_id>/', views.vacante_detail, name='vacante_detail'),
    path('vacante/create/', views.create_vacante, name='create_vacante'),
    path('vacantes/solicitadas/', views.vacantes_solicitadas, name='vacantes_solicitadas'),
    path('vacante/<int:vacante_id>/favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('vacantes/favoritas/', views.vacantes_favoritas, name='vacantes_favoritas'),
    # ... existing urls ...
] 