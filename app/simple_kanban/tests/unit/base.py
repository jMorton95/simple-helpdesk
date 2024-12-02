from django.test import TestCase
from django.contrib.auth.models import User
from simple_kanban.models import Project, Swimlane, Ticket

class BaseUnitTest(TestCase):
  def setUp(self):
    #Arrange
    self.user1 = User.objects.create_user(username="user1", password="ComplexPassword123!")
    self.user2 = User.objects.create_user(username="user2", password="ComplexPassword123!")
    self.project = Project.objects.create(name="ProjectOne", description="TestProject", created_by=self.user1)
    self.swimlane1 = Swimlane.objects.create(name="ToDo", sort_order=1, swimlane_project=self.project, created_by=self.user1)
    self.swimlane2 = Swimlane.objects.create(name="InProgress", sort_order=2, swimlane_project=self.project, created_by=self.user1)
    self.ticket1 = Ticket.objects.create(
      name="Ticket1",
      description="Description1",
      ticket_swimlane=self.swimlane1,
      ticket_priority=1,
      reporter=self.user1,
      assignee=self.user2,
      created_by=self.user1,
    )
    self.ticket2 = Ticket.objects.create(
      name="Ticket2",
      description="Description2",
      ticket_swimlane=self.swimlane2,
      ticket_priority=2,
      reporter=self.user2,
      created_by=self.user2,
    )
