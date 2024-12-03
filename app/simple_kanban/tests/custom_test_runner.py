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
    integration_tests = settings.BASE_DIR / "simple_kanban" / "tests" / "integration"
    unit_tests = settings.BASE_DIR / "simple_kanban" / "tests" / "unit"

    if not test_labels:
      suite.addTests(loader.discover(start_dir=str(integration_tests), pattern="test*.py"))
      suite.addTests(loader.discover(start_dir=str(unit_tests), pattern="test*.py"))
    else:
      suite = super().build_suite(test_labels, extra_tests, **kwargs)

    if extra_tests:
      suite.addTests(extra_tests)

    return suite
