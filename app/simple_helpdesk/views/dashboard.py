from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models import Project

@login_required(login_url="/register")
def dashboard(request):
  projects = Project.objects.all()
  context = {
    "projects": projects
  }
  
  return render(request, "helpdesk/index.html", context)