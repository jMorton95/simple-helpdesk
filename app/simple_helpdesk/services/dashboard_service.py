from simple_helpdesk.models import Project, Ticket

class DashboardService():
  
  def GetDashboardContext(request):
    projects = Project.objects.prefetch_related(
      'swimlane_set__ticket_set__ticketcomment_set'
    )

    tickets = Ticket.objects.prefetch_related('assignee', 'ticket_swimlane', 'ticketcomment_set')
    
    user_incidents = tickets.filter(assignee_id=request.user.id)
    related_incidents = tickets.exclude(assignee_id=request.user.id);
    
    return {
      "projects": projects,
      "user_incidents": user_incidents,
      "related_incidents": related_incidents
    }