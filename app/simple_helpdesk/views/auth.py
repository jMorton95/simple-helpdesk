from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, alogin
from simple_helpdesk.forms.login_form import LoginForm
from simple_helpdesk.utils.generic import validate_form
from simple_helpdesk.forms.register_form import RegisterForm
from simple_helpdesk.services.auth_service import AuthService

def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if validate_form(request, form):
      form.save()
      return redirect("index")
       
  return render(request, "authentication/register.html", {'form': RegisterForm})

def login(request):
  if request.method == "POST":
    form = LoginForm(request.POST)
    if validate_form(request, form):
      user = form.get_user()
      alogin(request, user)
      return redirect("index")
    
  return render(request, "authentication/login.html", {'form': LoginForm})