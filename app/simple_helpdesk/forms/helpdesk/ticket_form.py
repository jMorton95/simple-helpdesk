from django import forms
from simple_helpdesk.utils.constants import FORM_FIELD_CSS_CLASSES
from simple_helpdesk.models import Swimlane, Ticket
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
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
