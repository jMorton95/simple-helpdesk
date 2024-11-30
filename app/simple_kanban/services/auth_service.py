from simple_kanban.utils.generic import form_is_valid
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User


class AuthenticationService():
  def register(request, form):
    if form_is_valid(request, form):
      form.save()
      login(request, User.objects.filter(username = request.POST["email"]).first())
      return True
    else:
      return False
    
  def sign_in(request, form):
     if form_is_valid(request, form):
      login(request, form.get_user())
      return True
     else:
      return False
  
  def change_password(request, form):
     if form_is_valid(request, form):
      form.save()
      update_session_auth_hash(request, form.user)
      return True