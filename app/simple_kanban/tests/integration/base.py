from django.test import TestCase
from django.contrib.auth.models import User
from simple_kanban.models import Project

"""
  Configure default data for each Integration Test.
"""
class BaseIntegrationTest(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username="testuser", password="testpassword")
    self.client.login(username="testuser", password="testpassword")
    
    self.project = Project.objects.create(
      name="Test Project",
      description="Test Description",
      created_by=self.user
    )