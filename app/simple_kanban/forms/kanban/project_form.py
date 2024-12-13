from simple_kanban.utils.constants import FORM_FIELD_CSS_CLASSES
from simple_kanban.models import Project
from django import forms


class ProjectForm(forms.ModelForm):
  """
    Custom form to represent a Project Model.
    Widgets define the HTML Form element to be used and configures them with client-side validation.
  """
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