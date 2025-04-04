from .models import RecruiterProfile

def recruiter_context(request):
    """
    Añade la variable is_recruiter al contexto global de todas las plantillas.
    """
    is_recruiter = False
    if request.user.is_authenticated:
        is_recruiter = RecruiterProfile.objects.filter(user=request.user).exists()
    
    return {
        'is_recruiter': is_recruiter
    } 