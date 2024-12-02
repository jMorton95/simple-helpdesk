from simple_kanban.models import Project, Swimlane, Ticket
from simple_kanban.tests.unit.base import BaseUnitTest

class ProjectUnitTests(BaseUnitTest):
  def test_create_project_with_swimlanes_and_tickets(self):
    """
      Test the creation of the related Project, Swimlane and Ticket entities. 
      See simple_kanban/tests/integration/base.py.
    """
    print("Testing Projects, Swimlanes and Ticket Creation")
    
    #Assertions
    self.assertEqual(self.project.swimlanes.count(), 2)
    self.assertIsNotNone(self.project.created_at)
    self.assertEqual(self.swimlane1.tickets.count(), 1)
    self.assertEqual(self.swimlane2.tickets.count(), 1)
    self.assertIsNotNone(self.swimlane1.created_at)
    self.assertEqual(self.ticket1.name, "Ticket1")
    self.assertEqual(self.ticket2.assignee, None)
    self.assertIsNotNone(self.ticket1.created_at)
    print("Assertions Passed")
    
  def test_get_project_with_swimlanes_and_tickets(self):
    """
      Test the creation of the related Project, Swimlane and Ticket entities. 
      See simple_kanban/tests/integration/base.py.
    """
    print("Testing Projects, Swimlanes and Ticket Creation")
    
    #Act
    db_project = Project.objects.get(pk=self.project.id)
    db_swimlane1 = Swimlane.objects.get(pk=self.swimlane1.id)
    db_swimlane2 = Swimlane.objects.get(pk=self.swimlane2.id)
    db_ticket1 = Ticket.objects.get(pk=self.ticket1.id)
    db_ticket2 = Ticket.objects.get(pk=self.ticket2.id)

    self.assertEqual(db_project.name, self.project.name, "Project name should match.")
    self.assertEqual(db_project.description, self.project.description, "Project description should match.")
    self.assertEqual(db_project.swimlanes.count(), 2, "Project should have exactly 2 swimlanes.")
    self.assertIsNotNone(db_project.created_at, "Project created_at timestamp should not be None.")
    self.assertEqual(db_project.created_by, self.user1, "Project should be created by user1.")
    self.assertFalse(db_project.deleted, "Project should not be marked as deleted.")

    self.assertEqual(db_swimlane1.name, self.swimlane1.name, "Swimlane1 name should match.")
    self.assertEqual(db_swimlane2.name, self.swimlane2.name, "Swimlane2 name should match.")
    self.assertEqual(db_swimlane1.swimlane_project, db_project, "Swimlane1 should belong to the correct project.")
    self.assertEqual(db_swimlane2.swimlane_project, db_project, "Swimlane2 should belong to the correct project.")
    self.assertIsNotNone(db_swimlane1.created_at, "Swimlane1 created_at timestamp should not be None.")
    self.assertEqual(db_swimlane1.sort_order, 1, "Swimlane1 sort_order should be 1.")
    self.assertEqual(db_swimlane2.sort_order, 2, "Swimlane2 sort_order should be 2.")

    self.assertEqual(db_ticket1.name, self.ticket1.name, "Ticket1 name should match.")
    self.assertEqual(db_ticket2.name, self.ticket2.name, "Ticket2 name should match.")
    self.assertEqual(db_ticket1.ticket_swimlane, db_swimlane1, "Ticket1 should belong to Swimlane1.")
    self.assertEqual(db_ticket2.ticket_swimlane, db_swimlane2, "Ticket2 should belong to Swimlane2.")
    self.assertEqual(db_ticket1.assignee, self.user2, "Ticket1 should be assigned to user2.")
    self.assertEqual(db_ticket2.reporter, self.user2, "Ticket2 should have user2 as the reporter.")
    self.assertFalse(db_ticket1.deleted, "Ticket1 should not be marked as deleted.")
    self.assertEqual(db_ticket1.ticket_priority, 1, "Ticket1 priority should be 1.")
    self.assertEqual(db_ticket2.ticket_priority, 2, "Ticket2 priority should be 2.")

    self.assertIsNotNone(db_ticket1.created_at, "Ticket1 created_at timestamp should not be None.")
    self.assertIsNotNone(db_ticket2.created_at, "Ticket2 created_at timestamp should not be None.")

    print("Assertions Passed")
