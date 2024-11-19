from simple_helpdesk.utils.constants import FORM_FIELD_CSS_CLASSES
from simple_helpdesk.models import Project
from django import forms

class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    fields = ['name', 'description']
    widgets = {
      "name": forms.TextInput(attrs={
        "class": FORM_FIELD_CSS_CLASSES, "required": True
      }),
      "description": forms.Textarea(attrs={
        "rows": 4, "cols": 40, "class": FORM_FIELD_CSS_CLASSES, "required": True
      })
    }