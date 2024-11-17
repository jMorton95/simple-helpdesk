from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from simple_helpdesk.utils.auth import is_admin
from simple_helpdesk.services.project_service import ProjectService
from simple_helpdesk.services.dashboard_service import DashboardService
from simple_helpdesk.forms.helpdesk.project_form import ProjectForm
from simple_helpdesk.models import Swimlane
from simple_helpdesk.forms.helpdesk.swimlane_form import SwimlaneFormSet

@login_required(login_url="/register")
def index(request):
  context = DashboardService.GetDashboardContext(request)
  
  return render(request, "helpdesk/dashboard.html", context)

@login_required(login_url="/register")

def create_project(request):
  if request.method == "POST":
      if ProjectService.CreateProject(request):
        return redirect("index")
 
  context = ProjectService.GetProjectContext(request, False)

  return render(request, "helpdesk/project_form.html", context)


def edit_project(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(project_id)
  if not result: return redirect("404")
  
  if request.method == "POST":
    if ProjectService.EditProject(request, project):
      return redirect("index")
 
  context = ProjectService.GetProjectContext(request, True, project)

  return render(request, "helpdesk/project_form.html", context)

@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_project(request, project_id):
  [result, project] = ProjectService.GetProjectIfExists(project_id)
  if not result: 
    return redirect("404")
  else:
    project.soft_delete(request.user)
    
  return redirect("index")

@user_passes_test(is_admin, login_url="/", redirect_field_name=None)
def delete_swimlane(request, project_id, swimlane_id):
  [result, swimlane] = ProjectService.GetSwimlaneIfExists(swimlane_id)
  if not result: 
    return redirect("404")
  else:
    swimlane.soft_delete(request.user)
  
  return redirect("project_edit", project_id)
