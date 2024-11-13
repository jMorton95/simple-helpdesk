from django.contrib import messages
from django.contrib.auth.models import User

def validate_form(request, form) -> bool:
  try:
   for _, errors in form.errors.items():
        for error in errors:
          messages.error(request, error)
   return form.is_valid()
  except:
   return False

class AuthService:
  def register(request, form) -> bool:
    if validate_form(request, form):
      form.save()
      return True
    else:
      #messages.error(request, "An account with this email address already exists")
      return False
  