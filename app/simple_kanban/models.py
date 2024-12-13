from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


"""
  This module defines all database Models used throughout the application.
"""

"""
'Manager' Classes override DJango's Object Relational Mappers default behaviour of returning Database objects from queries.

These are used to define global filtering and sorting behaviour depending on the entity.
"""
class ActiveManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter(deleted=False)
  
class SwimlaneActiveManager(ActiveManager):
  def get_queryset(self):
    return super().get_queryset().filter(deleted=False).order_by('sort_order')

class TicketActiveManager(ActiveManager):
  def get_queryset(self):
    return super().get_queryset().filter(deleted=False).order_by('ticket_priority') 


"""
  The AuditableEntity abstract base class is used as a polymorphic template for all entities of the application.
  
  It defines fields that show logs of what has happened to each entity, such as when and who created, updated or deleted entities.
"""
class AuditableEntity(models.Model):
  """
    Fields are defined using DJango's 'model' framework.
    Each field is configured with ForeignKeys, default behaviours, nullability and deletion dehaviour.
  """
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)screated_by")
  created_at = models.DateTimeField(auto_now_add=True, blank=True)
  updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)supdated_by")
  updated_at = models.DateTimeField(auto_now=True)
  deleted = models.BooleanField(default=False)
  deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)sdeleted_by")
  deleted_at = models.DateTimeField(null=True, blank=True)
 
  objects = ActiveManager()
  
  class Meta:
    abstract = True
  
  def create(self, user):
    """
      Overrides default Create behaviour to record which user Created an Enity 
    """
    self.created_by = user
    self.save()
  
  def update(self, user, **kwargs):
    """
      Overrides default Update behaviour to record Auditable properties.
    """
    self.updated_by = user
    for field, value in kwargs.items():
      setattr(self, field, value)
    self.save()
    
  def soft_delete(self, user):
    """
      Custom deletion behaviour that causes entities to be globally filterd from all Read requests.
      Enables data integrity over time, can be extended in the future to automatically clean up deleted behaviour over a specific age.
    """
    self.deleted = True
    self.deleted_by = user
    self.deleted_at = timezone.now()
    self.save()
    
  def restore(self):
    """
      Restores a previously soft_delete()'d entity.
    """
    self.deleted = False
    self.deleted_by = None
    self.deleted_at = None
    self.save()



class Project(AuditableEntity):
  """
    Master entity of the application.
    Defines a compositional one-to-many relationship with Swimlanes.
  """
  name = models.CharField(max_length=40)
  description = models.CharField(max_length=1000)
  
  def __str__(self):
    return self.name
  
  @property
  def swimlanes(self):
    return self.swimlane_set.all()
    
    

class Swimlane(AuditableEntity):
  """
    Entity that logically groups Tickets and Projects.
    
    Defines a compositional one-to-many relationship with Tickets.
  """
  name = models.CharField(max_length=40)
  sort_order = models.IntegerField(default = 1)
  swimlane_project = models.ForeignKey(Project, on_delete=models.CASCADE)
  
  #Hooks into the SwimlaneActiveManager to automatically order Swimlanes by their sort_order property.
  objects = SwimlaneActiveManager()
  
  def __str__(self):
    return f"{self.swimlane_project.name} - {self.name}"
  
  @property
  def tickets(self):
    return self.ticket_set.all()
  
  def create(self, project, user):
    """
      Ensures the link between a Swimlane and Project is created at creation.
    """
    self.swimlane_project = project
    super().create(user)


class Ticket(AuditableEntity):
  """
    This entity serves as the primary store of data for the application.

    Defines a compositional one-to-many relationship with TicketComments
  """
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=1000)
  reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ticket_reporter")
  assignee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="ticket_assignee")
  ticket_swimlane = models.ForeignKey(Swimlane, on_delete=models.CASCADE)
  ticket_priority = models.IntegerField(default=1)
  
  objects = TicketActiveManager()
  
  def __str__(self):
    return f"{self.ticket_swimlane.swimlane_project.name} - {self.ticket_swimlane.name} - {self.name}"
  
  @property
  def comments(self):
    return self.ticketcomment_set.all()
  
  def create(self, swimlane, user):
    """
      Ensures a relationship with the Swimlane is created on creation.
    """
    self.ticket_swimlane = swimlane
    super().create(user)
    

class TicketComment(AuditableEntity):
  """
    Entity that allows a discussion between users on each Ticket.
  """
  text = models.CharField(max_length=2500)
  parent_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
  
  def __str__(self):
    return f"Comment: {self.user.username} - {self.parent_ticket.name}"


class ErrorLog(AuditableEntity):
  """
    Unrelated entity used to record warnings/errors throughout the application.
  """
  level = models.CharField(max_length=50)
  message = models.CharField(max_length=2500)