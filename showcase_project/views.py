from django.shortcuts import render
# from django.core 
from .models import AboutProject, Feature, SubFeature
# Create your views here.

def about(request):
    
    project_detail = None
    try:
        project_detail = AboutProject.objects.get(is_active=True)
    except:
        project_detail = AboutProject.objects.last()
    context = {
        'project_detail': project_detail,
    }
    return render(request, 'index.html', context)