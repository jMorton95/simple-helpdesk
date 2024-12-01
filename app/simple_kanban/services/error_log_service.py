
from simple_kanban.models import ErrorLog



class ErorrLogService():
  severity = ["Critical", "Warning", "Info", "Debug"]

  @staticmethod
  def get_severity(level: int):
    if len(ErorrLogService.severity) < level:
      raise ValueError("Severity Level not found.")
    else:
      return ErorrLogService.severity[level]
    
  @staticmethod
  def write_log_to_db(request, level: int, message: str):
    try:
      log_entry = ErrorLog(level=ErorrLogService.get_severity(level), message=message)
      return log_entry.create(request.user)
    except Exception as ex:
      return print(f"Critical Error occurred when adding log: {message}")