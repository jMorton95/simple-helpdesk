from unittest import TestLoader

def load_tests(loader, tests, pattern):
  suite = loader.discover(start_dir="simple_kanban/tests/integration", pattern="test*.py")
  suite.addTests(loader.discover(start_dir="simple_kanban/tests/unit", pattern="test*.py"))
  return suite