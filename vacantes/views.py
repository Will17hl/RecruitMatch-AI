from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vacante, Profile, Recruiter, RecruiterProfile, Postulacion
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import CustomUserCreationForm, ProfileForm, VacanteForm, RecruiterProfileForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def home(request):
    vacantes = Vacante.objects.all().order_by('-date')[:3]
    return render(request, 'home.html', {'vacantes': vacantes})

def vacantes_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    
    vacantes = Vacante.objects.all()
    
    if query:
        vacantes = vacantes.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(description__icontains=query)
        )
    
    if location:
        vacantes = vacantes.filter(location__icontains=location)
    
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(vacantes, 18)  # 18 vacantes por página
    
    try:
        vacantes = paginator.page(page)
    except PageNotAnInteger:
        vacantes = paginator.page(1)
    except EmptyPage:
        vacantes = paginator.page(paginator.num_pages)
    
    return render(request, 'vacantes_list.html', {
        'vacantes': vacantes,
        'query': query,
        'location': location
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil de reclutador si el usuario se registra como reclutador
            if form.cleaned_data['user_type'] == 'recruiter':
                RecruiterProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a RecruitMatch AI.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    # Verificar si el usuario es reclutador
    try:
        recruiter_profile = RecruiterProfile.objects.get(user=request.user)
        is_recruiter = True
        account_type = "Reclutador"
    except RecruiterProfile.DoesNotExist:
        is_recruiter = False
        account_type = "Cliente"
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tus datos se han guardado exitosamente!')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'account_type': account_type,
        'is_recruiter': is_recruiter
    }
    return render(request, 'profile.html', context)

@login_required
def recruiter_profile(request):
    try:
        profile = RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        profile = RecruiterProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = RecruiterProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tus datos se han guardado exitosamente!')
            return redirect('recruiter_profile')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = RecruiterProfileForm(instance=profile)
    return render(request, 'recruiter_profile.html', {'form': form, 'profile': profile})

def vacante_detail(request, pk):
    vacante = get_object_or_404(Vacante, pk=pk)
    ya_postulado = False
    estado_postulacion = None
    
    if request.user.is_authenticated:
        try:
            postulacion = Postulacion.objects.get(usuario=request.user, vacante=vacante)
            ya_postulado = True
            estado_postulacion = postulacion.estado
        except Postulacion.DoesNotExist:
            pass

    if request.method == 'POST' and request.user.is_authenticated:
        if not ya_postulado:
            Postulacion.objects.create(usuario=request.user, vacante=vacante)
            messages.success(request, '¡Te has postulado exitosamente a esta vacante!')
            return redirect('vacante_detail', pk=pk)
        else:
            messages.warning(request, 'Ya te has postulado a esta vacante anteriormente.')

    return render(request, 'vacante_detail.html', {
        'vacante': vacante,
        'ya_postulado': ya_postulado,
        'estado_postulacion': estado_postulacion
    })

@login_required
def create_vacante(request):
    # Verificar si el usuario es un reclutador
    try:
        recruiter_profile = RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        messages.error(request, 'Solo los reclutadores pueden crear vacantes.')
        return redirect('vacantes_list')

    if request.method == 'POST':
        form = VacanteForm(request.POST)
        if form.is_valid():
            vacante = form.save(commit=False)
            vacante.user = request.user
            vacante.date = timezone.now()
            vacante.save()
            messages.success(request, '¡La vacante se ha creado exitosamente!')
            return redirect('vacante_detail', pk=vacante.pk)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = VacanteForm()
    return render(request, 'create_vacante.html', {'form': form})

def vacante_list(request):
    vacantes = Vacante.objects.all().order_by('-date')
    return render(request, 'vacante_list.html', {'vacantes': vacantes})

@login_required
def vacantes_solicitadas(request):
    postulaciones = Postulacion.objects.filter(usuario=request.user).select_related('vacante')
    return render(request, 'vacantes_solicitadas.html', {
        'postulaciones': postulaciones
    })

@login_required
def toggle_favorito(request, pk):
    vacante = get_object_or_404(Vacante, id=pk)
    if request.user in vacante.favoritos.all():
        vacante.favoritos.remove(request.user)
        messages.success(request, 'Vacante eliminada de favoritos')
    else:
        vacante.favoritos.add(request.user)
        messages.success(request, 'Vacante agregada a favoritos')
    return redirect('vacante_detail', pk=vacante.id)

@login_required
def vacantes_favoritas(request):
    vacantes = request.user.vacantes_favoritas.all()
    return render(request, 'vacantes_favoritas.html', {
        'vacantes': vacantes
    })