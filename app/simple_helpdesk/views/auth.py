from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from simple_helpdesk.forms.auth.login_form import LoginForm
from simple_helpdesk.utils.generic import form_is_valid
from simple_helpdesk.forms.auth.register_form import RegisterForm
from simple_helpdesk.forms.auth.change_password_form import ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form_is_valid(request, form):
      form.save()
      login(request, User.objects.filter(username = request.POST["email"]).first())
      return redirect("index")
       
  return render(request, "authentication/register.html", {'form': RegisterForm})


def sign_in(request):
  if request.method == "POST":
    form = LoginForm(data=request.POST)
    if form_is_valid(request, form):
      login(request, form.get_user())
      return redirect("index")
    
  return render(request, "authentication/sign_in.html", {'form': LoginForm})


def sign_out(request):
  logout(request)
  return redirect("sign_in")


@login_required(login_url="/register")
def change_password(request):
  if request.method == "POST":
    form = ChangePasswordForm(user=request.user, data=request.POST)
    if form_is_valid(request, form):
      form.save()
      update_session_auth_hash(request, form.user)
      return redirect("index")
      
  return render(request, "authentication/change_password.html", {'form': ChangePasswordForm(user=request.user)})