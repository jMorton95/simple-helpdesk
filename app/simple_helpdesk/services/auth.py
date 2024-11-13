from django.contrib import messages
from django.contrib.auth.models import User


class AuthService:
  def register(request, form) -> bool:
    if not form.is_valid():  
      for i in form.error_messages:
        messages.error(request, i)
      return False
        
    if not User.objects.filter(username = form.cleaned_data['email']).exists():
      form.save()
      return True
    else:
      messages.error(request, "An account with this email address already exists")
    
    return False