from django.shortcuts import render, redirect
from django.contrib.auth import logout
from simple_kanban.services.auth_service import AuthenticationService
from simple_kanban.forms.auth.login_form import LoginForm
from simple_kanban.forms.auth.register_form import RegisterForm
from simple_kanban.forms.auth.change_password_form import ChangePasswordForm
from django.contrib.auth.decorators import login_required


def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if AuthenticationService.register(request, form):
      return redirect("index")
       
  return render(request, "authentication/register.html", {'form': RegisterForm})


def sign_in(request):
  if request.method == "POST":
    form = LoginForm(data=request.POST)
    if AuthenticationService.sign_in(request, form):
      return redirect("index")
    
  return render(request, "authentication/sign_in.html", {'form': LoginForm})


def sign_out(request):
  logout(request)
  return redirect("sign_in")

@login_required(login_url="/register")
def change_password(request):
  if request.method == "POST":
    form = ChangePasswordForm(user=request.user, data=request.POST)
    if AuthenticationService.change_password(request, form):
      return redirect("index")
      
  return render(request, "authentication/change_password.html", {'form': ChangePasswordForm(user=request.user)})