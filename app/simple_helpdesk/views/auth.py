from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from simple_helpdesk.forms.login_form import LoginForm
from simple_helpdesk.utils.generic import validate_form
from simple_helpdesk.forms.register_form import RegisterForm
from simple_helpdesk.forms.change_password_form import ChangePasswordForm
from simple_helpdesk.services.auth_service import AuthService

def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if validate_form(request, form):
      form.save()
      return redirect("index")
       
  return render(request, "authentication/register.html", {'form': RegisterForm})

def sign_in(request):
  if request.method == "POST":
    form = LoginForm(data=request.POST)
    
    if validate_form(request, form):
      login(request, form.get_user())
      return redirect("index")
    
  return render(request, "authentication/sign_in.html", {'form': LoginForm})

def sign_out(request):
  logout(request)
  return redirect("sign_in")

def change_password(request):
  if request.method == "POST":
    form = ChangePasswordForm(user=request.user, data=request.POST)
    if validate_form(request, form):
        form.save()
        update_session_auth_hash(request, form.user)
        return redirect("index")
      
  return render(request, "authentication/change_password.html", {'form': ChangePasswordForm(user=request.user)})