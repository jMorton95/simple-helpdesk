from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from simple_kanban.services.toast_service import ToastService
from simple_kanban.utils.generic import redirect_with_toast
from simple_kanban.utils.auth import is_admin
from simple_kanban.services.ticket_service import TicketService
from simple_kanban.services.swimlane_service import SwimlaneService
from simple_kanban.services.project_service import ProjectService
from simple_kanban.services.dashboard_service import DashboardService

@login_required(login_url="/register")
def index(request):
  context = DashboardService.GetDashboardContext(request)
  
  return render(request, "kanban/dashboard.html", context)

@login_required(login_url="/register")
def create_project(request):
  if request.method == "POST":
    if ProjectService.CreateProject(request):
      return redirect_with_toast(request, "index", "Success", "Succesfully created project.")
 
  context = ProjectService.GetProjectFormContext(request, False)

  return render(request, "kanban/project_form.html", context)

@login_required(login_url="/register")
def edit_project(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(request, project_id)
  if not result:
    return redirect_with_toast(request, "index", "Not Found", "The selected project could not be found.")
  
  if request.method == "POST":
    if ProjectService.EditProject(request, project):
      ToastService.send_toast_message(request, "Success", "Succesfully saved project.")
     
  context = ProjectService.GetProjectFormContext(request, True, project)
  
  return render(request, "kanban/project_form.html", context)

@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_project(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(request, project_id)
  if not result: 
    return redirect_with_toast(request, "index", "Not Found", "Could not delete Project as it no longer exists.")
  
  project.soft_delete(request.user)
  SwimlaneService.DeleteProjectSwimlanes(request, project)
    
  return redirect_with_toast(request, "index", "Success", "Succesfully deleted Project")

@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_swimlane(request, project_id, swimlane_id):
  [result, swimlane] = SwimlaneService.GetSwimlaneIfExists(request, swimlane_id)
  if not result: 
    return redirect_with_toast(request, "index", "Not Found", "Could not delete Swimlane as it no longer exists.")
  
  swimlane.soft_delete(request.user)
  TicketService.DeleteSwimlaneTickets(request, swimlane)
  
  return redirect_with_toast(request, "project_edit", "Success", "Succesfully deleted Swimlane", project_id)
