from django.shortcuts import render
from ..models import Project

def index(request):
  context = { "project": Project.objects.first() }
  return render(request, "helpdesk/index.html", context)

