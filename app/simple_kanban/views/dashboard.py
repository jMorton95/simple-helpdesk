from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from simple_kanban.models import Project, Swimlane
from simple_kanban.services.toast_service import ToastService
from simple_kanban.utils.generic import get_object_if_exists, redirect_with_toast
from simple_kanban.utils.auth import is_admin
from simple_kanban.services.ticket_service import TicketService
from simple_kanban.services.swimlane_service import SwimlaneService
from simple_kanban.services.project_service import ProjectService
from simple_kanban.services.dashboard_service import DashboardService


"""
  Module that contains all endpoints related to viewing the Dashboard
  and creating/editing Project entities.
  
  @login_required attribute enforces an active authentication session to access the endpoint.
  @user_passes_test attribute invokes custom function that checks if a user is admin, rejects request if criteria is not met.
"""

@login_required(login_url="/register")
def index(request):
  """
    Retrieves all data for the system to present to the User.
  """
  context = DashboardService.GetDashboardContext(request)
  
  return render(request, "kanban/dashboard.html", context)


@login_required(login_url="/register")
def create_project(request):
  """
    Retrieves an Empty Create Project Form if GET request.
    Otherwise, creates a new Project if POST request.
    
    Displays errors to the UI if Project could not be created.
  """
  if request.method == "POST":
    if ProjectService.CreateProject(request):
      return redirect_with_toast(request, "index", "Success", "Succesfully created project.")
 
  context = ProjectService.GetProjectFormContext(request, False)

  return render(request, "kanban/project_form.html", context)


@login_required(login_url="/register")
def edit_project(request, project_id):
  """
    Retrieves a requested Project to populate an Edit Project Form if Request is GET.
    
    Action is invoked when a User submits an Edit Project form and request is POST.
    
    Displays errors to the UI if Project could not be found, or edited.
  """
  [result, project] = get_object_if_exists(request, Project, project_id)
  if not result:
    return redirect_with_toast(request, "index", "Not Found", "The selected project could not be found.")
  
  if request.method == "POST":
    if ProjectService.EditProject(request, project):
      ToastService.send_toast_message(request, "Success", "Succesfully saved project.")
     
  context = ProjectService.GetProjectFormContext(request, True, project)
  
  return render(request, "kanban/project_form.html", context)


@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_project(request, project_id):
  """
    Invokved when Admin users raise a delete request for a specific Project.
    Redirects to the Dashboard if the Project could not be found.
    
    Deletes all entities related to the Project and then redirects to the Dashboard.
  """
  [result, project] = get_object_if_exists(request, Project, project_id)
  if not result: 
    return redirect_with_toast(request, "index", "Not Found", "Could not delete Project as it no longer exists.")
  
  project.soft_delete(request.user)
  SwimlaneService.DeleteProjectSwimlanes(request, project)
    
  return redirect_with_toast(request, "index", "Success", "Succesfully deleted Project")


@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_swimlane(request, project_id, swimlane_id):
  """
    Invokved when Admin users raise a delete request for a specific Swimlane.
    Redirects to the Dashboard if the Swimlane could not be found.
    
    Deletes all entities related to the Swimlane and then redirects to the Dashboard.
  """
  [result, swimlane] = get_object_if_exists(request, Swimlane, swimlane_id)
  if not result: 
    return redirect_with_toast(request, "index", "Not Found", "Could not delete Swimlane as it no longer exists.")
  
  swimlane.soft_delete(request.user)
  TicketService.DeleteSwimlaneTickets(request, swimlane)
  
  return redirect_with_toast(request, "project_edit", "Success", "Succesfully deleted Swimlane", project_id)
