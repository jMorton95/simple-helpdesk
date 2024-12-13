from django.shortcuts import render, redirect
from django.contrib.auth import logout
from simple_kanban.services.auth_service import AuthenticationService
from simple_kanban.forms.auth.login_form import LoginForm
from simple_kanban.forms.auth.register_form import RegisterForm
from simple_kanban.forms.auth.change_password_form import ChangePasswordForm
from django.contrib.auth.decorators import login_required


"""
  Module that contains all endpoints related Authentication.
  and creating/editing Project entities.
  
  @login_required attribute enforces an active authentication session to access the endpoint.
  Endpoints not marked with @login_required attribute are publicly accessible.
"""

def register(request):
  """
    Creates an Empty Registration Form is request is GET.
    
    Otherwise Submits a Registration Form is request is POST.
    
    If successfully registered, redirects to Dashboard.
  """
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if AuthenticationService.register(request, form):
      return redirect("index")
       
  return render(request, "authentication/register.html", {'form': RegisterForm})


def sign_in(request):
  """
    Creates an Empty Sign In form is request is GET.
    
    Otherwise Submits a Sign In form is request is POST
    
    If sign in is succesful, redirects to Dashboard.
  """
  if request.method == "POST":
    form = LoginForm(data=request.POST)
    if AuthenticationService.sign_in(request, form):
      return redirect("index")
    
  return render(request, "authentication/sign_in.html", {'form': LoginForm})

@login_required(login_url="/register")
def sign_out(request):
  """
    Immediately signs a user out and destroys their session.
    
    Redirects to the sign in page.
  """
  logout(request)
  return redirect("sign_in")


@login_required(login_url="/register")
def change_password(request):
  """
    Creates an empty Change Password form is request is GET.
    
    Otherwise submits a Change Password form is request is POST.
    
    Creates a new session and redirects to the Dashboard if succesful, otherwise displays errors to user.
  """
  if request.method == "POST":
    form = ChangePasswordForm(user=request.user, data=request.POST)
    if AuthenticationService.change_password(request, form):
      return redirect("index")
      
  return render(request, "authentication/change_password.html", {'form': ChangePasswordForm(user=request.user)})