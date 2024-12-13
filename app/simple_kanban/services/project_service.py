from django.db.models import Prefetch
from simple_kanban.utils.auth import CreateUserContext
from simple_kanban.models import Project, Swimlane, Ticket, TicketComment
from simple_kanban.forms.kanban.project_form import ProjectForm
from simple_kanban.forms.kanban.swimlane_form import SwimlaneFormSet
from simple_kanban.utils.generic import form_is_valid


class ProjectService():
  """
    This class provides an abstraction over CRUD operations involving Projects.
    As Swimlanes are treated as a property of a Project, they are also managed within the ProjectService.
    
    Methods do not rely on instance state and are treated as static. 
  """
  
  def GetProjectFormContext(request, is_update: bool, project: Project | None = None):
    """
      Populates the DJango Context for Create and Edit project forms.
      Form instances are populated with a Project if editing, or empty if creating.
    """
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
  
  
  def GetProjectContext(request, project: Project):
    """
      Populates the DJango context for views reliant on a Project entity. 
      Nested queries retrieve all related swimlane, ticket and comment entities.
    """
    project_data = Project.objects.prefetch_related(
        Prefetch('swimlane_set', queryset=Swimlane.objects.prefetch_related(
            Prefetch('ticket_set', queryset=Ticket.objects.prefetch_related(
                'assignee', 'reporter',
                Prefetch('ticketcomment_set', queryset=TicketComment.objects.select_related('user')
            ))
        ))
    )).filter(id=project.id).first()
    
    return CreateUserContext(request, {
        'project': project_data,
        'swimlanes': project_data.swimlane_set.all(),
    })
  
  
  def CreateProject(request) -> bool:
    """
      Responsible for validating and creating a new Project when a Project form is submitted.
      This first instantiates forms from request data, validates both forms, saves the Project and iteratively saves nested Swimlanes.
      
      Returns true/false to indicate the status of the operation.
    """
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
    """
      Responsible for validating and editing a Project when a Project Edit form is submitted.
      This first instantiates forms with request data and existing database entities.
      Next, forms are validated and iteratively saved with new data.
      
      Returns true/false to indicate the status of the operation.
    """
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