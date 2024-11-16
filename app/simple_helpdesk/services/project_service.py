from typing import Union
from simple_helpdesk.models import Project, Swimlane
from simple_helpdesk.forms.helpdesk.project_form import ProjectForm
from simple_helpdesk.forms.helpdesk.swimlane_form import SwimlaneFormSet
from simple_helpdesk.utils.generic import form_is_valid

class ProjectService():
  
  def GetProjectContext(is_update: bool, project: Project | None = None):
    project_form = ProjectForm(instance=project)
    swimlane_formset = SwimlaneFormSet(
      queryset=Swimlane.objects.filter(swimlane_project=project) if project 
      else Swimlane.objects.none())
    
    return {
        "project_form": project_form,
        "swimlane_formset": swimlane_formset,
        "is_update": is_update,
        "project": project
    }
  
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
              (swimlane_form
                .save(commit=False)
                .update(request.user))
      return True
    else: 
      return False
    
  def DeleteProject(request, project_id) -> Union[bool, str]:
    if not request.user.groups.filter(name="Admin").exists():
      return [False, f"User: {request.user.username} does not have access to this functionality."]
    else:
      Project.objects.get(pk=project_id).soft_delete(request.user)
      return [True, "Success"]
    
    
  def GetProjectIfExists(project_id) -> Union[bool, Project | None]:
    try:
      project = Project.objects.get(pk=project_id)
      return [True, project]
    except Project.DoesNotExist:
      return [False, None]
