import json
from django.contrib import messages


class ToastService():
  @staticmethod
  def send_toast_message(request, header: str, text: str):
    toast_data = {
        "toast_header": header,
        "toast_body_text": text,
        "message_type": "toast"
    }
    messages.add_message( request, messages.INFO, json.dumps(toast_data), extra_tags="toast")