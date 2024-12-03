from pathlib import Path
import sys
from django.test.runner import DiscoverRunner
from unittest import TestLoader, TestSuite

class CustomTestRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        loader = TestLoader()
        suite = TestSuite()
        
        # Get the app directory path
        project_root = Path(__file__).resolve().parent.parent.parent
        sys.path.insert(0, str(project_root))
        print("root")
        print(project_root)
        
        if not test_labels:
            integration_tests = project_root / "simple_kanban/tests/integration"
            unit_tests = project_root / "simple_kanban/tests/unit"
            
            print(f"Looking for tests in:\n{integration_tests}\n{unit_tests}")
            
            if not integration_tests.is_dir() or not unit_tests.is_dir():
                raise ValueError(f"Test directories not found:\n{integration_tests}\n{unit_tests}")
            
            for test_dir in [integration_tests.parent, integration_tests, unit_tests]:
                init_file = test_dir / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
            
            suite.addTests(loader.discover(
                start_dir=str(integration_tests),
                pattern="test*.py",
                top_level_dir=str(project_root)
            ))
            
            suite.addTests(loader.discover(
                start_dir=str(unit_tests),
                pattern="test*.py",
                top_level_dir=str(project_root)
            ))
        else:
            suite = super().build_suite(test_labels, extra_tests, **kwargs)

        if extra_tests:
            suite.addTests(extra_tests)

        return suite