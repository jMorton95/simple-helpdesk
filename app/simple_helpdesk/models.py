from django.db import models
from django.contrib.auth.models import User

class AuditableEntity:
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_by")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_by")
  updated_at = models.DateTimeField(auto_now=True)
  deleted = models.BooleanField(default=False)
  deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="deleted_by")
  deleted_at = models.DateTimeField(null=True)

class Project(models.Model, AuditableEntity):
  name = models.CharField(max_length=40)
  description = models.CharField(max_length=1000)
  
  @property
  def swimlanes(self):
    return self.swimlane_set.all()
    
class Swimlane(models.Model, AuditableEntity):
  name = models.CharField(max_length=40)
  sort_order = models.IntegerField(default = 1)
  swimlane_project = models.ForeignKey(Project, on_delete=models.CASCADE)
  
  @property
  def tickets(self):
    return self.ticket_set.all()


class Ticket(models.Model, AuditableEntity):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=1000)
  reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ticket_reporter")
  assignee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="ticket_assignee")
  ticket_swimlane = models.ForeignKey(Swimlane, on_delete=models.CASCADE)
  ticket_priority = models.IntegerField(default=1)
  
  @property
  def comments(self):
    return self.ticketcomment_set.all()
    
class TicketComment(models.Model, AuditableEntity):
  text = models.CharField(max_length=2500)
  parent_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

