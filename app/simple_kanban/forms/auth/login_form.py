from django.contrib.auth.forms import AuthenticationForm
from simple_kanban.utils.constants import FORM_FIELD_CSS_CLASSES
class LoginForm(AuthenticationForm):
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['username'].widget.attrs.update({
        'class': FORM_FIELD_CSS_CLASSES,
        'placeholder': 'Please enter your Email Address',
        'id': 'username',
        'required': True,
    })
    
    self.fields['password'].widget.attrs.update({
        'class': FORM_FIELD_CSS_CLASSES,
        'placeholder': 'Please enter your Password',
        'id': 'password',
        'required': True,
    })