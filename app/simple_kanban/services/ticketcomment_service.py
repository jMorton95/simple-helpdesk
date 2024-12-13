from simple_kanban.utils.generic import form_is_valid
from simple_kanban.forms.kanban.ticketcomment_form import TicketCommentForm
from simple_kanban.models import TicketComment

class TicketCommentService():
  """
    Class that provides an abstraction over CRUD operations related to the TicketComment entity.
    
    Methods do not rely on instance state and are treated as static. 
  """
  
  def GetCommentCreateContext():
    """
      Method that creates a DJango context for an empty TicketComment Form.
    """
    comment_form = TicketCommentForm()
    return { "comment_form": comment_form, "comment_id": None}
  
  
  def GetCommentEditContext(ticketcomment):
    """
      Method that creates a DJango context for an empty TicketComment Form.
    """
    edit_comment_form = TicketCommentForm(instance=ticketcomment)
    comment_form = TicketCommentForm()
    return { "comment_form": comment_form, "edit_comment_form": edit_comment_form, "comment_id": ticketcomment.id }
  
  
  def CreateComment(request, ticket_id):
    """
      Method that is invoked when a User submits a TicketComment form.
      This constructs a form instance from the request, validates the form and saves it.
      
      Returns true/false to indicate the result of the operation.
    """
    comment_form = TicketCommentForm(data=request.POST)
    
    if form_is_valid(request, comment_form):
      comment_form.save(request, ticket_id)
      return True
    else:
      return False
  
  
  def EditComment(request, ticket_id, ticket_comment):
    """
      Method that resolves when a User submits an Edit TicketComment form.
      Comments are validated and then saved.
      
      Returns true/false to indicate the result of the operation.
    """
    comment_form = TicketCommentForm(data=request.POST, instance=ticket_comment)
    
    if form_is_valid(request, comment_form):
      comment = comment_form.save(request, ticket_id, commit=False)
      comment.update(request.user)
      return True
    else: 
      return False
  
  
  def DeleteTicketComments(request, ticket):
    """
      Method that deletes all comments related to a specific Ticket.
    """
    related_comments = TicketComment.objects.filter(parent_ticket=ticket)
    for comment in related_comments:
      comment.soft_delete(request.user)