from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from simple_helpdesk.utils.generic import form_is_valid
from simple_helpdesk.services.dashboard_service import DashboardService
from simple_helpdesk.forms.helpdesk.project_form import ProjectForm
from simple_helpdesk.models import Swimlane
from simple_helpdesk.forms.helpdesk.swimlane_form import SwimlaneFormSet

@login_required(login_url="/register")
def index(request):
  context = DashboardService.GetDashboardContext(request)
  
  return render(request, "helpdesk/dashboard.html", context)

def project(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        swimlane_formset = SwimlaneFormSet(request.POST)

        if form_is_valid(request, project_form) and form_is_valid(request, swimlane_formset):
            project = project_form.save(commit=False)
            project.created_by = request.user
            project.save()

            for swimlane_form in swimlane_formset:
                swimlane = swimlane_form.save(commit=False)
                swimlane.swimlane_project = project
                swimlane.save()

            return redirect("index")
    else:
        project_form = ProjectForm()
        swimlane_formset = SwimlaneFormSet(queryset=Swimlane.objects.none())

    return render(request, "helpdesk/project_create.html", {
        "project_form": project_form,
        "swimlane_formset": swimlane_formset
    })