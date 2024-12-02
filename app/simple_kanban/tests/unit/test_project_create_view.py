from django.urls import reverse
from simple_kanban.tests.unit.base import BaseUnitTest
from simple_kanban.models import Project

class CreateProjectViewTest(BaseUnitTest):

  def test_create_project_post(self):
    url = reverse('project_create')
    
    self.client.post(url, {
        'name': 'New Project',
        'description': 'A New Project Description',
    })
    
    self.assertEqual(Project.objects.count(), 1)
    self.assertEqual(Project.objects.last().name, 'New Project')

  def test_create_project_get(self):
    url = reverse('project_create')
    
    response = self.client.get(url)
    
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'kanban/project_form.html')
