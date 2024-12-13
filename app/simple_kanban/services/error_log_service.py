
from simple_kanban.models import ErrorLog


class ErorrLogService():
  """
    Class that provides an abstraction on Error Logging.
    
    Contains four log levels to enable log filtering.
  """
  severity = ["Critical", "Warning", "Info", "Debug"]

  def get_severity(level: int):
    """
      Retrieves the string from the Severity List by index.
      Raises an error if an invalid index is passed.
    """
    if len(ErorrLogService.severity) < level:
      raise ValueError("Severity Level not found.")
    else:
      return ErorrLogService.severity[level]
  
  def write_log_to_db(request, level: int, message: str):
    """
      Method exposed to consumers to simplify error logging.
      Composes an error log entity and saves it to the database.
      
      Example usage:
        write_log_to_db(request, 1, "Could not find entity")
    """
    try:
      log_entry = ErrorLog(level=ErorrLogService.get_severity(level), message=message)
      return log_entry.create(request.user)
    except Exception as ex:
      return print(f"Critical Error occurred when adding log: {message} - {str(ex)}")