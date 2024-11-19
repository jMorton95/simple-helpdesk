from django import forms
from simple_helpdesk.models import Swimlane, Ticket
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
  def __init__(self, request, project_id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['assignee'] = forms.ModelChoiceField(
      queryset=User.objects.all(),
      required=False,
      label="Assignee",
      widget=forms.Select(attrs={'class': 'form-control'})
    )
    self.fields['reporter'] = forms.ModelChoiceField(
      queryset=User.objects.all(),
      required=True,
      label="Reporter",
      initial=request.user,
      widget=forms.Select(attrs={'class': 'form-control'})
    )
    self.fields['ticket_swimlane'] = forms.ModelChoiceField(
      queryset=Swimlane.objects.filter(swimlane_project=project_id),
      required=True,
      label="Swimlane",
      widget=forms.Select(attrs={'class': 'form-control'})
    )
    self.fields['ticket_priority'] = forms.IntegerField(
      required=True,
      label="Priority",
      widget=forms.NumberInput(attrs={'class': 'form-control', "min": 1})
    )
    
  class Meta:
    model = Ticket
    fields = ["name", "description", "assignee", "reporter", "ticket_swimlane", "ticket_priority"]
