from typing import Union
from simple_helpdesk.services.ticket_service import TicketService
from simple_helpdesk.utils.generic import get_object_if_exists
from simple_helpdesk.models import Swimlane


class SwimlaneService():
  
  def GetSwimlaneIfExists(swimlane_id) -> Union[bool, Swimlane | None]:
    return get_object_if_exists(Swimlane, swimlane_id)
  
  def DeleteProjectSwimlanes(request, project):
    related_swimlanes = Swimlane.objects.filter(swimlane_project=project)
    for swimlane in related_swimlanes:
      TicketService.DeleteSwimlaneTickets(request, swimlane)
      swimlane.soft_delete(request.user)