from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from simple_helpdesk.utils.generic import merge_contexts
from simple_helpdesk.services.ticket_service import TicketService
from simple_helpdesk.services.project_service import ProjectService

@login_required(login_url="/register")
def overview(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(project_id)
  if not result:
    redirect("404")

  context = ProjectService.GetProjectContext(request, project)
  
  return render(request, "helpdesk/project_overview.html", context)

@login_required(login_url="/register")
def create_ticket_form(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(project_id)
  if not result:
    redirect("404")
    
  project_context = ProjectService.GetProjectContext(request, project)
  create_ticket_context = TicketService.GetCreateTicketContext(request, project_id)
  
  return render(request, "helpdesk/project_overview.html", merge_contexts(project_context, create_ticket_context))

@login_required(login_url="/register")
def create_ticket(request, project_id):
  if request.method == "POST":
    if TicketService.CreateTicket(request, project_id):
      return redirect("project_overview", project_id)
  
  return redirect("ticket_new", project_id)

def edit_ticket_form(request, project_id, ticket_id):
  [project_result, project] = ProjectService.GetProjectIfExists(project_id)
  [ticket_result, ticket] = TicketService.GetTicketIfExists(ticket_id)
  
  if not ticket_result or not project_result:
    redirect("404")
  
  project_context = ProjectService.GetProjectContext(request, project)
  edit_ticket_context = TicketService.GetEditTicketContext(request, ticket)
  
  return render (request, "helpdesk/project_overview.html", merge_contexts(project_context, edit_ticket_context))

@login_required(login_url="/register")
def edit_ticket(request, project_id, ticket_id):
  [ticket_result, ticket] = TicketService.GetTicketIfExists(ticket_id)
  
  if not ticket_result:
    redirect("404")
  
  if request.method == "POST":
    if TicketService.EditTicket(request, project_id, ticket):
      return redirect("project_overview", project_id)
  
  return redirect("ticket_view", project_id, ticket_id)