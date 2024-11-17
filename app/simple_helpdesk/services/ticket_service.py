from simple_helpdesk.services.ticketcomment_service import TicketCommentService
from simple_helpdesk.models import Ticket

class TicketService():
  def DeleteSwimlaneTickets(request, swimlane):
    related_tickets = Ticket.objects.filter(ticket_swimlane=swimlane)
    for ticket in related_tickets:
      TicketCommentService.DeleteTicketComments(request, ticket)
      ticket.soft_delete(request.user)