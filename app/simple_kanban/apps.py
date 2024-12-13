from django.apps import AppConfig

"""
  Hooks the Simple Kanban application module up to the DJango server.
"""
class SimpleKanbanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simple_kanban'
