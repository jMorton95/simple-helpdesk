from typing import Union
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode
from simple_kanban.services.error_log_service import ErorrLogService

def form_is_valid(request, form) -> bool:
  """
    Validates a form and displays any error messages.

    Iterates form errors and adds to Django's Messaging Framework.
    It then returns the result of the form.

    Args:
        request: The HTTP request object used to display error messages.
        form: Any form that inherits from Django's forms.ModelForm.

    Returns:
        bool: True if the form is valid, otherwise False.

    Example:
        if form_is_valid(request, my_form):
            # Continue processing
        else:
            # Handle invalid form
  """
  try:
    if form.errors and form.errors.items and len(form.errors.items()) > 0:
      for _, errors in form.errors.items():
          for error in errors:
            messages.error(request, error)
  except Exception as e:
    print(str(e))
  return form.is_valid()


def get_object_if_exists(request, model_class, object_id) -> Union[bool, object | None]:
  try:
      obj = model_class.objects.get(pk=object_id)
      return [True, obj]
  except model_class.DoesNotExist:
    ErorrLogService.write_log_to_db(
      request=request,
      level=2,
      message=f"{str(model_class.__name__)} with ID: {object_id} not found."
    )
    return [False, None]
    
def merge_contexts(*args) -> dict:
  new_context = {}
  for obj in args:
    if isinstance(obj, dict):
      new_context.update(obj)
  return new_context

def redirect_with_message(action: str, name: str, message: str):
  """
    Redirect to a named action (see simple_kanban/urls.py) action with a query parameter encoded message to the UI.
    
    Typically used for redirecting a 404 error back to a page with descriptive message. 
  """
  return redirect(f"{reverse(action)}?{urlencode({name: message})}")