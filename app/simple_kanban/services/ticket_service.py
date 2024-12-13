from simple_kanban.utils.generic import form_is_valid
from simple_kanban.forms.kanban.ticket_form import TicketForm
from simple_kanban.services.ticketcomment_service import TicketCommentService
from simple_kanban.models import Ticket


class TicketService():
  """
    This Class provides an abstraction over CRUD operations related to the Ticket entity.
    
    Methods do not rely on instance state and are treated as static. 
  """
  
  def GetCreateTicketContext(request, project_id):
    """
      Method that creates a DJango context for a Create TicketForm
    """
    ticket_form = TicketForm(request, project_id)
    return {
      "ticket_form": ticket_form,
      "create_ticket": True
    }
  
  
  def GetEditTicketContext(request, ticket):
    """
      Method that creates a DJango context for a Create TicketForm
    """
    ticket_form = TicketForm(request, ticket.ticket_swimlane.swimlane_project.id, instance=ticket)
    return {
      "ticket_form": ticket_form,
      "ticket": ticket,
      "edit_ticket": True
    }
    
  def CreateTicket(request, project_id):
    """
      Method that resolves when a User submits a Create Ticket form.
      Tickets are validated and then saved.
      
      Returns true/false to indicate the result of the operation.
    """
    ticket_form = TicketForm(request, project_id, data=request.POST)
    
    if form_is_valid(request, ticket_form):
      ticket = ticket_form.save(commit=False)
      ticket.create(ticket.ticket_swimlane, request.user)
      return True
    else:
      return False
    
  def EditTicket(request, project_id, ticket):
    """
      Method that resolves when a User submits an Edit Ticket form.
      Tickets are validated and then saved.
      
      Returns true/false to indicate the result of the operation.
    """
    ticket_form = TicketForm(request, project_id, data=request.POST, instance=ticket)
    
    if form_is_valid(request, ticket_form):
      ticket = ticket_form.save(commit=False)
      ticket.update(request.user)
      return True
    else: 
      return False
    
  
  def DeleteSwimlaneTickets(request, swimlane):
    """
      Method responsible for finding and deleting all Tickets related to a Swimlane.
      This also iteratively deletes all Comments related to Tickets.
    """
    related_tickets = Ticket.objects.filter(ticket_swimlane=swimlane)
    for ticket in related_tickets:
      TicketCommentService.DeleteTicketComments(request, ticket)
      ticket.soft_delete(request.user)