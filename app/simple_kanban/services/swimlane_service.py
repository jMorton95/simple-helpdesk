from simple_kanban.services.ticket_service import TicketService
from simple_kanban.models import Swimlane


class SwimlaneService():
  """
    Class that provides an abstraction over CRUD operations specifically related to Swimlanes.
    
    Methods do not rely on instance state and are treated as static. 
  """
  
  def DeleteProjectSwimlanes(request, project):
    """
      Method that deletes all Swimlanes from a specific Project.
      This finds all Swimlanes related to a Project and iterates over them, deleting their Tickets before deleting the Swimlane.
    """
    related_swimlanes = Swimlane.objects.filter(swimlane_project=project)
    for swimlane in related_swimlanes:
      TicketService.DeleteSwimlaneTickets(request, swimlane)
      swimlane.soft_delete(request.user)