from django import forms
from django.forms import modelformset_factory
from simple_helpdesk.models import Project, Swimlane

class SwimlaneForm(forms.ModelForm):
    class Meta:
        model = Swimlane
        fields = ['name', 'sort_order']

SwimlaneFormSet = modelformset_factory(Swimlane, form=SwimlaneForm, extra=0)