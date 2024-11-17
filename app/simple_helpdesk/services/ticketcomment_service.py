from simple_helpdesk.models import TicketComment

class TicketCommentService():
  def DeleteTicketComments(request, ticket):
    related_comments = TicketComment.objects.filter(parent_ticket=ticket)
    for comment in related_comments:
      comment.soft_delete(request.user)