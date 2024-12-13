from simple_kanban.utils.generic import form_is_valid
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User


class AuthenticationService():
  """
    This class provides an abstraction over Authentication actions.
    Methods do not rely on instance state and are treated as static. 
  """
  
  def register(request, form):
    """
      Validate the form, then log the new user in.
    """
    if form_is_valid(request, form):
      form.save()
      login(request, User.objects.filter(username = request.POST["email"]).first())
      return True
    else:
      return False
    
  def sign_in(request, form):
    """
      Validate the form, then log the user in.
    """
    if form_is_valid(request, form):
      login(request, form.get_user())
      return True
    else:
      return False
  
  def change_password(request, form):
    """
      Validate the form, update the user session from new hashed instance data. 
    """
    if form_is_valid(request, form):
      form.save()
      update_session_auth_hash(request, form.user)
      return True