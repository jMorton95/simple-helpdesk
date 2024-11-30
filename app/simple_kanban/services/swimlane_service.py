from typing import Union
from simple_kanban.services.ticket_service import TicketService
from simple_kanban.utils.generic import get_object_if_exists
from simple_kanban.models import Swimlane


class SwimlaneService():
  
  def GetSwimlaneIfExists(request, swimlane_id) -> Union[bool, Swimlane | None]:
    return get_object_if_exists(request, Swimlane, swimlane_id)
  
  def DeleteProjectSwimlanes(request, project):
    related_swimlanes = Swimlane.objects.filter(swimlane_project=project)
    for swimlane in related_swimlanes:
      TicketService.DeleteSwimlaneTickets(request, swimlane)
      swimlane.soft_delete(request.user)