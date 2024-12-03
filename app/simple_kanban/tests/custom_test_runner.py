from pathlib import Path
import sys
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

    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    if not test_labels:
        integration_tests = project_root / "tests/integration"
        unit_tests = project_root / "tests/unit"

        suite.addTests(loader.discover(start_dir=str(integration_tests), pattern="test*.py"))
        suite.addTests(loader.discover(start_dir=str(unit_tests), pattern="test*.py"))
    else:
        suite = super().build_suite(test_labels, extra_tests, **kwargs)

    if extra_tests:
        suite.addTests(extra_tests)

    return suite
