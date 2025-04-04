from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from vacantes.views import home, register, profile, recruiter_profile, vacante_detail, create_vacante, vacantes_list, vacantes_solicitadas, vacantes_favoritas, toggle_favorito

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('recruiter-profile/', recruiter_profile, name='recruiter_profile'),
    path('vacantes/', vacantes_list, name='vacantes_list'),
    path('vacante/<int:pk>/', vacante_detail, name='vacante_detail'),
    path('vacante/create/', create_vacante, name='create_vacante'),
    path('vacantes/solicitadas/', vacantes_solicitadas, name='vacantes_solicitadas'),
    path('vacante/<int:pk>/favorito/', toggle_favorito, name='toggle_favorito'),
    path('vacantes/favoritas/', vacantes_favoritas, name='vacantes_favoritas'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)