from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from simple_kanban.models import Project, Ticket, TicketComment
from simple_kanban.utils.auth import is_admin
from simple_kanban.services.ticketcomment_service import TicketCommentService
from simple_kanban.utils.generic import get_object_if_exists, merge_contexts, redirect_with_toast
from simple_kanban.services.ticket_service import TicketService
from simple_kanban.services.project_service import ProjectService

"""
  Module that contains all endpoints related to viewing and
  creating data that is related to Project entities.
  For example, Tickets and Ticket Comments.
"""

@login_required(login_url="/register")
def overview(request, project_id):
  [result, project] = get_object_if_exists(request, Project, project_id)
  if not result:
    return redirect_with_toast(request, "index", "Not Found", "The selected project could not be found.")

  context = ProjectService.GetProjectContext(request, project)
  
  return render(request, "kanban/project_overview.html", context)


@login_required(login_url="/register")
def create_ticket_form(request, project_id):
  [result, project] = get_object_if_exists(request, Project, project_id)
  if not result:
    return redirect_with_toast(request, "index", "Not Found", "Cannot create a Ticket as project no longer exists.")
    
  project_context = ProjectService.GetProjectContext(request, project)
  create_ticket_context = TicketService.GetCreateTicketContext(request, project_id)
  
  return render(request, "kanban/project_overview.html", merge_contexts(project_context, create_ticket_context))


@login_required(login_url="/register")
def create_ticket(request, project_id):
  if request.method == "POST":
    if TicketService.CreateTicket(request, project_id):
      return redirect_with_toast(request, "project_overview", "Success", "Successfully created Ticket.", project_id)
  
  return redirect("ticket_new", project_id)


def edit_ticket_form(request, project_id, ticket_id):
  [project_result, project] = get_object_if_exists(request, Project, project_id)
  [ticket_result, ticket] = get_object_if_exists(request, Ticket, ticket_id)
  
  if not ticket_result or not project_result:
    return redirect_with_toast(request, "index", "Not Found", "The selected Project and/or Ticket could not be found.")
  
  project_context = ProjectService.GetProjectContext(request, project)
  edit_ticket_context = TicketService.GetEditTicketContext(request, ticket)
  comment_context = TicketCommentService.GetTicketCreateContext()
  
  return render(request, "kanban/project_overview.html", merge_contexts(project_context, edit_ticket_context, comment_context))


@login_required(login_url="/register")
def edit_ticket(request, project_id, ticket_id):
  if request.method == "POST":
    [ticket_result, ticket] = get_object_if_exists(request, Ticket, ticket_id)
  
    if not ticket_result:
      return redirect_with_toast(request, "index", "Not Found", "The selected Ticket could not be found.")
  
    if TicketService.EditTicket(request, project_id, ticket):
      return redirect_with_toast(request, "project_overview", "Success", f"Succesfully updated {ticket.name}", project_id)
  
  return redirect("ticket_view", project_id, ticket_id)


@login_required(login_url="/register")
def add_comment(request, project_id, ticket_id):
  if request.method == "POST":
    [ticket_result, _] = get_object_if_exists(request, Ticket, ticket_id)
    
    if not ticket_result:
      return redirect_with_toast(request, "index", "Not Found", "Could not add comment as Ticket no longer exists.")
      
    TicketCommentService.CreateComment(request, ticket_id)
  
  return redirect_with_toast(request, "ticket_view", "Success", "Succesfully added comment.", project_id, ticket_id)


@login_required(login_url="/register")
def edit_comment(request, project_id, ticket_id, ticketcomment_id):
  if request.method == "POST":
    [comment_result, comment] = get_object_if_exists(request, TicketComment, ticketcomment_id)
    
    if not comment_result:
      return redirect_with_toast(request, "index", "Not Found", "Could not edit comment as it no longer exists.")
      
    TicketCommentService.EditComment(request, comment)
  
  return redirect_with_toast(request, "ticket_view", "Success", "Succesfully added comment.", project_id, ticket_id)


@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_ticket(request, project_id, ticket_id):
  [result, ticket] = get_object_if_exists(request, Ticket, ticket_id)
  
  if not result:
    return redirect_with_toast(request, "index", "Not Found", "Could not delete Ticket as it no longer exists.")
  
  ticket.soft_delete(request.user)
  TicketCommentService.DeleteTicketComments(request, ticket)
  
  return redirect_with_toast(request, "project_overview", "Success", "Successfully deleted ticket.", project_id)


@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_comment(request, project_id, ticket_id, ticketcomment_id):
  [result, comment] = get_object_if_exists(request, TicketComment, ticketcomment_id)
  
  if not result:
    return redirect_with_toast(request, "index", "Not Found", "Could not delete Comment as it no longer exists.")
    
  comment.soft_delete(request.user)
  
  return redirect_with_toast(request, "ticket_view", "Success", "Succesfully deleted comment.", project_id, ticket_id)