from typing import Union
from simple_helpdesk.services.ticket_service import TicketService
from simple_helpdesk.utils.auth import CreateUserContext, is_admin
from simple_helpdesk.models import Project, Swimlane, Ticket, TicketComment
from simple_helpdesk.forms.helpdesk.project_form import ProjectForm
from simple_helpdesk.forms.helpdesk.swimlane_form import SwimlaneFormSet
from simple_helpdesk.utils.generic import form_is_valid, get_object_if_exists

class ProjectService():
  
  def __init__(self):
    pass
  
  def GetProjectContext(request, is_update: bool, project: Project | None = None):
    project_form = ProjectForm(instance=project)
    swimlane_formset = SwimlaneFormSet(
      queryset=Swimlane.objects.filter(swimlane_project=project) if project 
      else Swimlane.objects.none())
    
    return CreateUserContext(request, {
        "project_form": project_form,
        "swimlane_formset": swimlane_formset,
        "is_update": is_update,
        "project": project
    })
  
  def CreateProject(request) -> bool:
    project_form = ProjectForm(request.POST)
    swimlane_formset = SwimlaneFormSet(request.POST)
    
    if form_is_valid(request, project_form) and form_is_valid(request, swimlane_formset):
      project = project_form.save(commit=False)
      project.create(request.user)

      for swimlane_form in swimlane_formset:
          if swimlane_form.cleaned_data:
              (swimlane_form
                .save(commit=False)
                .create(project, request.user))
      return True
    else: 
      return False
    
  def EditProject(request, project) -> bool:
    project_form = ProjectForm(request.POST, instance=project)
    swimlane_formset = SwimlaneFormSet(request.POST, queryset=Swimlane.objects.filter(swimlane_project=project))
    
    if form_is_valid(request, project_form) and form_is_valid(request, swimlane_formset):
      project = project_form.save(commit=False)
      project.update(request.user)
      
      for swimlane_form in swimlane_formset:
          if swimlane_form.cleaned_data:
              swimlane = swimlane_form.save(commit=False)
              swimlane.swimlane_project = project
              swimlane.update(request.user)
      return True
    else: 
      return False
  
  def GetProjectIfExists(project_id) -> Union[bool, Project | None]:
    return get_object_if_exists(Project, project_id)

 
    
  
