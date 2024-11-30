
from simple_kanban.models import ErrorLog


class ErorrLogService():
  severity = ["Critical", "Warning", "Info", "Debug"]

  def get_severity(this, level: int):
    if len(this.severity) < level:
      raise ValueError("Severity Level not found.")
    else:
      return this.severity[level]
  
  def write_log_to_db(this, request, level: int, message: str):
    try:
      log_entry = ErrorLog(level = this.get_severity(level), message=message)
      return log_entry.create(request)
    except:
      return print(f"Critical Error occurred when adding log: {message}")
  

