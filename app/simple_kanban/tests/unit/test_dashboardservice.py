from simple_kanban.services.dashboard_service import DashboardService
from simple_kanban.tests.unit.base import BaseUnitTest

class DashboardServiceUnitTests(BaseUnitTest):
  def test_get_dashboard_context(self):
    """
      Test the GetDashboardContext method for filtering tickets by user.
    """
    print("Testing GetDashboardContext for user-specific ticket filtering")

    class MockRequest:
      user = self.user2

    request = MockRequest()

    context = DashboardService.GetDashboardContext(request)

    user_incidents = context['user_incidents']
    related_incidents = context['related_incidents']

    self.assertEqual(user_incidents.count(), 1, "User2 should have exactly 1 ticket assigned.")
    self.assertIn(self.ticket1, user_incidents, "Ticket1 should be in user_incidents.")
    self.assertNotIn(self.ticket2, user_incidents, "Ticket2 should not be in user_incidents.")

    self.assertEqual(related_incidents.count(), 1, "User1 should have exactly 1 related incident.")
    self.assertIn(self.ticket2, related_incidents, "Ticket2 should be in related_incidents.")
    self.assertNotIn(self.ticket1, related_incidents, "Ticket1 should not be in related_incidents.")

    projects = context['projects']
    self.assertEqual(projects.count(), 1, "There should be exactly 1 project in the context.")
    self.assertIn(self.project, projects, "The project should be in the projects list.")

    print("All assertions passed!")
