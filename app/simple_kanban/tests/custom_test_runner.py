import os
from django.test.runner import DiscoverRunner
from unittest import TestLoader, TestSuite
from pathlib import Path
from django.conf import settings

class CustomTestRunner(DiscoverRunner):
  """
  A custom test runner to include subdirectories for integration and unit tests.
  """

  def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
    """
    Build a test suite using test discovery for specified test paths.
    """
    loader = TestLoader()
    suite = TestSuite()

    # Use Path to construct the test directories
    tests_root = os.path.join(settings.BASE_DIR, "../simple_kanban/tests")
    integration_tests = os.path.join(tests_root, "integration")
    unit_tests = os.path.join(tests_root, "unit")
    
    print(f"Integration tests path: {integration_tests}")
    print(f"Unit tests path: {unit_tests}")

    if not test_labels:
      suite.addTests(loader.discover(start_dir=str(integration_tests), pattern="test*.py"))
      suite.addTests(loader.discover(start_dir=str(unit_tests), pattern="test*.py"))
    else:
      suite = super().build_suite(test_labels, extra_tests, **kwargs)

    if extra_tests:
      suite.addTests(extra_tests)

    return suite
