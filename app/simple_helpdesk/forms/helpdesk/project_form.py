from simple_helpdesk.models import Project
from django import forms

class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    fields = ['name', 'description']
    widgets = {
      "name": forms.TextInput(attrs={
        "class": "form-control", "required": True
      }),
      "description": forms.Textarea(attrs={
        "rows": 4, "cols": 40, "class": "form-control", "required": True
      })
    }