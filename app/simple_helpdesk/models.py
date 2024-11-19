from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class ActiveManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter(deleted=False)
  
class SwimlaneActiveManager(ActiveManager):
  def get_queryset(self):
    return super().get_queryset().filter(deleted=False).order_by('sort_order')

class AuditableEntity(models.Model):
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
    self.created_by = user
    self.save()
  
  def update(self, user, **kwargs):
    self.updated_by = user
    for field, value in kwargs.items():
      setattr(self, field, value)
    self.save()
    
  def soft_delete(self, user):
    self.deleted = True
    self.deleted_by = user
    self.deleted_at = timezone.now()
    self.save()
    
  def restore(self):
    self.deleted = False
    self.deleted_by = None
    self.deleted_at = None
    self.save()

class Project(AuditableEntity):
  name = models.CharField(max_length=40)
  description = models.CharField(max_length=1000)
  
  def __str__(self):
    return self.name
  
  @property
  def swimlanes(self):
    return self.swimlane_set.all()
    
class Swimlane(AuditableEntity):
  name = models.CharField(max_length=40)
  sort_order = models.IntegerField(default = 1)
  swimlane_project = models.ForeignKey(Project, on_delete=models.CASCADE)
  
  objects = SwimlaneActiveManager()
  
  def __str__(self):
    return f"{self.swimlane_project.name} - {self.name}"
  
  @property
  def tickets(self):
    return self.ticket_set.all()
  
  def create(self, project, user):
    self.swimlane_project = project
    super().create(user)
  


class Ticket(AuditableEntity):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=1000)
  reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ticket_reporter")
  assignee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="ticket_assignee")
  ticket_swimlane = models.ForeignKey(Swimlane, on_delete=models.CASCADE)
  ticket_priority = models.IntegerField(default=1)
  
  def __str__(self):
    return f"{self.ticket_swimlane.swimlane_project.name} - {self.ticket_swimlane.name} - {self.name}"
  
  @property
  def comments(self):
    return self.ticketcomment_set.all()
    
class TicketComment(AuditableEntity):
  text = models.CharField(max_length=2500)
  parent_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
  
  def __str__(self):
    return f"Comment: {self.user.username} - {self.parent_ticket.name}"

