import json
from django.contrib import messages


class ToastService():
  """
    Class that provides an abstraction over displaying Toaster messages to the User.
  """
  
  @staticmethod
  def send_toast_message(request, header: str, text: str):
    """
      Creates a JSON object that will be serialised into a message passed to the User Interface.
      Messages are passed with DJango's messaging framework.
    """
    toast_data = {
        "toast_header": header,
        "toast_body_text": text,
        "message_type": "toast"
    }
    messages.add_message( request, messages.INFO, json.dumps(toast_data), extra_tags="toast")