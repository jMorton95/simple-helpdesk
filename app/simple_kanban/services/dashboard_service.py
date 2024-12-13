from simple_kanban.models import Project, Ticket


class DashboardService():
  """
    Class that provides an abstraction over generating the Dashboard Content.
    Methods do not rely on instance state and are treated as static. 
  """
  def GetDashboardContext(request):
    """
      Method that generates the Django context with all application data.
      
      First retrieves all Projects with related Swimlanes, Tickets and Comments.
      Next, retrieves all Foreign Keys related to Tickets.
      Next, creates two dicts for tickets assigned, and not assigned to the current user.
    """
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