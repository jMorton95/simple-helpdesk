from simple_helpdesk.models import Project, Swimlane, Ticket
from django.db.models import Prefetch


class DashboardService():
  
  def GetDashboardContext():
    projects = Project.objects.prefetch_related(
      'swimlane_set__ticket_set__ticketcomment_set'
    )
  
    return {"projects": projects}