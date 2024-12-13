from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from simple_kanban.utils.constants import FORM_FIELD_CSS_CLASSES

class RegisterForm(UserCreationForm):
  """
    Custom RegisterForm that overrides DJango's UserCreationForm.
    Error messages are specified with Meta and the custom "admin" property extends UserCreationForm.
    
    Widget.attrs specifies custom CSS classes and Placeholders.
  """
  admin = forms.BooleanField(required=False, label="Administrator")
  class Meta:
      model = User
      fields = ("email", "password1", "password2")
      
      error_messages = {
        "password2": {
          "common_password": "Password too common. Please increase the complexity of your password"
        } 
      }
        
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['email'].widget.attrs.update({
        'class': FORM_FIELD_CSS_CLASSES,
        'placeholder': 'Your email address',
        'id': 'email',
        'required': True,
    })
    
    self.fields['password1'].widget.attrs.update({
        'class': FORM_FIELD_CSS_CLASSES,
        'placeholder': 'Password',
        'id': 'password1',
        'required': True,
    })
    
    self.fields['password2'].widget.attrs.update({
        'class': FORM_FIELD_CSS_CLASSES,
        'placeholder': 'Confirm Password',
        'id': 'password2',
        'required': True,
    })
    
  def clean(self):
    """
      Override UserCreationForm's clean() method.
      This first performs a custom comparison to ensure passwords are matching.
      Next, a DB operation scans for existing accounts with the same email address, erroring if found. 
    """
    cleaned_data = super().clean()

    password1 = cleaned_data.get('password1')
    password2 = cleaned_data.get('password2')

    if password1 and password2 and password1 != password2:
      self.add_error('password2', "The two password fields didn’t match. Please enter matching passwords.")
        
    if User.objects.filter(username = cleaned_data.get('email')).exists():
      self.add_error('email', "A user account with this email address already exists.")
    
    return cleaned_data

  def save(self, commit=True):
    """
      Overrides the UserCreationForm.save() method.
      Instantiate the Model instance, then set the username property to the email address.
        This is required as Django prefers username authentication by default.
      Finally, if User is to be created as admin, create the role if it does not exist then add the user to it.
    """
    user = super().save(commit=False)
    user.username = user.email
    if commit:
      user.save()
    
    if self.cleaned_data.get('admin'):
      admin_group, _ = Group.objects.get_or_create(name='Admin')  
      user.groups.add(admin_group)
      user.save()
      
    return user