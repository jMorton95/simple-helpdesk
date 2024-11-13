from django.contrib import messages
from django.contrib.auth.models import User
from simple_helpdesk.utils.generic import validate_form

class AuthService:
  def register(request, form) -> bool:
    if validate_form(request, form):
      form.save()
      return True
    else:
      return False
    
  def login(request, form) -> bool:
    if validate_form(request, form):
      user = form.get_user()
  