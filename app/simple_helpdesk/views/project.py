from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from simple_helpdesk.services.ticket_service import TicketService
from simple_helpdesk.services.swimlane_service import SwimlaneService
from simple_helpdesk.services.project_service import ProjectService

@login_required(login_url="/register")
def overview(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(project_id)
  if not result:
    redirect("404")

  context = ProjectService.GetProjectContext(request, project)
  
  return render(request, "helpdesk/project_overview.html", context)