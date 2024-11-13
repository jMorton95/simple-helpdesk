from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
        
        error_messages = {
        "password_mismatch": "The two password fields didn’t match. Please enter matching passwords.",
        "username": {
            "unique": "This username is already taken. Please choose a different one.",
        },
    }
        
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      self.fields['email'].widget.attrs.update({
          'class': 'form-control',
          'placeholder': 'Your email address',
          'id': 'email',
          'required': True,
      })
      
      self.fields['password1'].widget.attrs.update({
          'class': 'form-control',
          'placeholder': 'Password',
          'id': 'password1',
          'required': True,
      })
      
      self.fields['password2'].widget.attrs.update({
          'class': 'form-control',
          'placeholder': 'Confirm Password',
          'id': 'password2',
          'required': True,
      })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user