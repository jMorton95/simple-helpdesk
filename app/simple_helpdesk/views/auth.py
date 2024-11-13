from django.shortcuts import render, redirect
from simple_helpdesk.forms.register_form import RegisterForm

from simple_helpdesk.services.auth import AuthService

def register(request):
  if request.method == "POST":
    if AuthService.register(request, RegisterForm(request.POST)):
      return redirect("")
       
  return render(request, "authentication/register.html", {'form': RegisterForm})

def login(request):
  return render(request, "authentication/login.html")