from simple_kanban.tests.unit.base import BaseUnitTest
from django.urls import reverse

class DashboardViewTest(BaseUnitTest):
  def test_index_view(self):
    url = reverse('index')
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Test Project")
    self.assertTemplateUsed(response, 'kanban/dashboard.html')