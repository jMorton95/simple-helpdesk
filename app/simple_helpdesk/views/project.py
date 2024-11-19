from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from simple_helpdesk.utils.generic import merge_contexts
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

@login_required(login_url="/register")
def create_ticket(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(project_id)
  if not result:
    redirect("404")
    
  project_context = ProjectService.GetProjectContext(request, project)
  create_ticket_context = TicketService.GetCreateTicketContext(request, project_id)
  
  return render(request, "helpdesk/project_overview.html", merge_contexts(project_context, create_ticket_context))