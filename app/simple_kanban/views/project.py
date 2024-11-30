from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from simple_kanban.utils.auth import is_admin
from simple_kanban.services.ticketcomment_service import TicketCommentService
from simple_kanban.utils.generic import merge_contexts, redirect_with_message
from simple_kanban.services.ticket_service import TicketService
from simple_kanban.services.project_service import ProjectService
from django.contrib import messages

@login_required(login_url="/register")
def overview(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(project_id)
  if not result:
    return redirect_with_message("index", "redirect_message", "The selected project could not be found.")

  context = ProjectService.GetProjectContext(request, project)
  
  return render(request, "helpdesk/project_overview.html", context)

@login_required(login_url="/register")
def create_ticket_form(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(project_id)
  if not result:
    return redirect_with_message("index", "redirect_message", "Cannot create a Ticket as project no longer exists.")
    
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
    return redirect_with_message("index", "redirect_message", "The selected Project and/or Ticket could not be found.")
  
  project_context = ProjectService.GetProjectContext(request, project)
  edit_ticket_context = TicketService.GetEditTicketContext(request, ticket)
  comment_context = TicketCommentService.GetTicketCreateContext()
  
  return render (request, "helpdesk/project_overview.html", merge_contexts(project_context, edit_ticket_context, comment_context))

@login_required(login_url="/register")
def edit_ticket(request, project_id, ticket_id):
  if request.method == "POST":
    [ticket_result, ticket] = TicketService.GetTicketIfExists(ticket_id)
  
    if not ticket_result:
      return redirect_with_message("index", "redirect_message", "The selected Ticket could not be found.")
  
    if TicketService.EditTicket(request, project_id, ticket):
      return redirect("project_overview", project_id)
  
  return redirect("ticket_view", project_id, ticket_id)

@login_required(login_url="/register")
def add_comment(request, project_id, ticket_id):
  if request.method == "POST":
    [ticket_result, _] = TicketService.GetTicketIfExists(ticket_id)
    
    if not ticket_result:
      return redirect_with_message("index", "redirect_message", "Could not add comment as Ticket no longer exists.")
      
    TicketCommentService.CreateComment(request, ticket_id)
  
  return redirect("ticket_view", project_id, ticket_id)

@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_ticket(request, project_id, ticket_id):
  [result, ticket] = TicketService.GetTicketIfExists(ticket_id)
  
  if not result:
    return redirect_with_message("index", "redirect_message", "Could not delete Ticket as it no longer exists.")
  
  ticket.soft_delete(request.user)
  TicketCommentService.DeleteTicketComments(request, ticket)
  
  return redirect("project_overview", project_id)

@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_comment(request, project_id, ticket_id, ticketcomment_id):
  [result, comment] = TicketCommentService.GetCommentIfExists(ticketcomment_id)
  
  if not result:
    return redirect_with_message("index", "redirect_message", "Could not delete Comment as it no longer exists.")
    
  comment.soft_delete(request.user)
  
  return redirect("ticket_view", project_id, ticket_id)