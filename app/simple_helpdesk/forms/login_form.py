from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['username'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Please enter your Email Address',
        'id': 'username',
        'type': 'email',
        'required': True,
    })
    
    self.fields['password'].widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Please enter your Password',
        'id': 'password',
        'type': 'password',
        'required': True,
    })