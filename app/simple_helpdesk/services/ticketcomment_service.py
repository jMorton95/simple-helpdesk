from simple_helpdesk.utils.generic import form_is_valid
from simple_helpdesk.forms.helpdesk.ticketcomment_form import TicketCommentForm
from simple_helpdesk.models import TicketComment

class TicketCommentService():
  def DeleteTicketComments(request, ticket):
    related_comments = TicketComment.objects.filter(parent_ticket=ticket)
    for comment in related_comments:
      comment.soft_delete(request.user)
    
  def GetTicketCreateContext():
    comment_form = TicketCommentForm()
    return { "comment_form": comment_form }
  
  def CreateComment(request, ticket_id):
    comment_form = TicketCommentForm(data=request.POST)
    
    if form_is_valid(request, comment_form):
      comment_form.save(request, ticket_id)
      return True
    else:
      return False