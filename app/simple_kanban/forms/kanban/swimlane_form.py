from django import forms
from django.forms import modelformset_factory
from simple_kanban.models import Swimlane


class SwimlaneForm(forms.ModelForm):
  """
    Custom form to represent a Swimlane Model.
    Widgets define the HTML Form element to be used and configures them with client-side validation.
  """
  class Meta:
    model = Swimlane
    fields = ['name', 'sort_order']
    widgets = {
      "name": forms.TextInput(attrs={
        "class": "form-control"
      }),
      "sort_order": forms.NumberInput(attrs={
        "class": "form-control", "min": 1
      })
    }
    
#SwimlaneFormSet defines a collection of Swimlane Forms. Used to create multiple Swimlanes when creating/editing a project simultaneously
SwimlaneFormSet = modelformset_factory(Swimlane, form=SwimlaneForm, extra=0)