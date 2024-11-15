from simple_helpdesk.models import Project, Swimlane, Ticket
from django.db.models import Prefetch


class DashboardService():
  
  def GetDashboardContext(request):
    projects = Project.objects.prefetch_related(
      'swimlane_set__ticket_set__ticketcomment_set'
    )

    user_incidents = Ticket.objects.filter(assignee_id=request.user.id).prefetch_related('assignee', 'ticket_swimlane', 'ticketcomment_set')  
    
    return {"projects": projects, "user_incidents": user_incidents}