import os
from django.test.runner import DiscoverRunner
from unittest import TestLoader, TestSuite

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

    # Get the absolute path to the tests directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    integration_tests = os.path.join(base_dir, "integration")
    unit_tests = os.path.join(base_dir, "unit")

    if not test_labels:
      suite.addTests(loader.discover(start_dir=integration_tests, pattern="test*.py"))
      suite.addTests(loader.discover(start_dir=unit_tests, pattern="test*.py"))
    else:
      suite = super().build_suite(test_labels, extra_tests, **kwargs)

    if extra_tests:
      suite.addTests(extra_tests)

    return suite
