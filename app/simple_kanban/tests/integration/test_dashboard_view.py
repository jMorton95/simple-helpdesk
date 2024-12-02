from simple_kanban.tests.integration.base import BaseIntegrationTest
from django.urls import reverse

class DashboardViewIntegrationTest(BaseIntegrationTest):
  def test_index_view(self):
    url = reverse('index')
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Test Project")
    self.assertTemplateUsed(response, 'kanban/dashboard.html')