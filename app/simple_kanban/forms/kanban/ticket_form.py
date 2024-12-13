from django import forms
from simple_kanban.utils.constants import FORM_FIELD_CSS_CLASSES
from simple_kanban.models import Swimlane, Ticket
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
  """
    Custom form to represent a Ticket Model.
    
    __init__ Defines HTML form elements used for all fields of the Model.
    Configures each HTML field with classes, and client-side validation rules.
      __init__ is used here instead of the usual standard Class Meta as DB operations must occur before the form can be instantiated.
  """
  def __init__(self, request, project_id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'] = forms.CharField(
      label="Name",
      required=True,
      widget=forms.TextInput(attrs={'class': FORM_FIELD_CSS_CLASSES,  "min": 4, "max": 25})
    )
    self.fields['description'] = forms.CharField(
      label="Description",
      required=True,
      widget=forms.TextInput(attrs={'class': FORM_FIELD_CSS_CLASSES, "rows": 4, "cols": 40, min: 10, max: 255})
    )
    #ModelChoiceField represents a HTML Select/Dropdown Box. Queryset is provides the selectable options, in this case all Users in the system.
    self.fields['assignee'] = forms.ModelChoiceField(
      queryset=User.objects.all(),
      required=False,
      label="Assignee",
      widget=forms.Select(attrs={'class': FORM_FIELD_CSS_CLASSES})
    )
    self.fields['reporter'] = forms.ModelChoiceField(
      queryset=User.objects.all(),
      required=True,
      label="Reporter",
      initial=request.user,
      widget=forms.Select(attrs={'class': FORM_FIELD_CSS_CLASSES})
    )
    #ModelChoiceField represents a HTML Select/Dropdown Box. Queryset is provides the selectable options, in this case all Swimlanes assigned to the Project.
    self.fields['ticket_swimlane'] = forms.ModelChoiceField(
      queryset=Swimlane.objects.filter(swimlane_project=project_id),
      required=True,
      label="Swimlane",
      widget=forms.Select(attrs={'class': FORM_FIELD_CSS_CLASSES})
    )
    self.fields['ticket_priority'] = forms.IntegerField(
      required=True,
      label="Priority",
      initial=1,
      widget=forms.NumberInput(attrs={'class': FORM_FIELD_CSS_CLASSES, "min": 1})
    )
    
  class Meta:
    model = Ticket
    fields = ["name", "description", "assignee", "reporter", "ticket_swimlane", "ticket_priority"]
