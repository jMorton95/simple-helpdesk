from django.db import models
from dataclasses import dataclass
from django.contrib.auth.models import User

@dataclass
class AuditableEntity:
  created_by = models.ForeignKey(User)
  created_at = models.DateTimeField()
  updated_by = models.ForeignKey(User)
  updated_at = models.DateTimeField()
  deleted = models.BooleanField(default=False)
  deleted_by = models.ForeignKey(User)
  deleted_at = models.DateTimeField(null=True)

@dataclass
class Project(models.Model, AuditableEntity):
  name = models.CharField(max_length=40)
  description = models.CharField(max_length=1000)
    
@dataclass
class Swimlane(models.Model, AuditableEntity):
  name = models.CharField(max_length=40)
  sort_order = models.IntegerField(default = 1)
  swimlane_project = models.ForeignKey(Project, models.CASCADE)

@dataclass
class TicketPriority(models.Model, AuditableEntity):
  name = models.CharField(max_length=25)
  sort_order = models.IntegerField(default = 1)
  colour = models.CharField(max_length = 10)

@dataclass
class Ticket(models.Model, AuditableEntity):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=1000)
  reporter = models.ForeignKey(User, models.SET_NULL, null=True)
  assignee = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
  ticket_swimlane = models.ForeignKey(Swimlane, models.CASCADE)
  ticket_priority = models.ForeignKey(TicketPriority)
    
@dataclass
class TicketComment(models.Model, AuditableEntity):
  text = models.CharField(max_length=2500)
  parent_ticket = models.ForeignKey(Ticket, models.CASCADE)

