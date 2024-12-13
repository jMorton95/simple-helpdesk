from django import forms
from simple_kanban.utils.constants import FORM_FIELD_CSS_CLASSES
from simple_kanban.models import TicketComment


class TicketCommentForm(forms.ModelForm):
  """
    Custom Form for to represent a TicketComment.
    HTML Form Fields are configured with CSS classes and client-side validation properties.
  """
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
    """
      Override the default on save() behaviour.
      Use the HTTP request to determine the user and ticket to assign the comment to.
    """
    comment = super().save(commit)
    comment.user_id = request.user.id
    comment.parent_ticket_id = ticket_id
    comment.create(request.user)
    return comment
    