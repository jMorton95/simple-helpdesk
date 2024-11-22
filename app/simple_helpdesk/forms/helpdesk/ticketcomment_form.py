from django import forms
from simple_helpdesk.utils.constants import FORM_FIELD_CSS_CLASSES
from simple_helpdesk.models import TicketComment


class TicketCommentForm(forms.ModelForm):
  
  class Meta:
    model = TicketComment
    fields = ["text"]
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.fields['text'] = forms.CharField(
      required=True,
      label="",
      help_text="",
      widget=forms.TextInput(attrs={'class': FORM_FIELD_CSS_CLASSES,  "min": 0, "max": 255})
    )
    
  def save(self, request, ticket_id, commit=False):
    comment = super().save(commit)
    comment.user_id = request.user.id
    comment.parent_ticket_id = ticket_id
    comment.create(request.user)
    return comment
    