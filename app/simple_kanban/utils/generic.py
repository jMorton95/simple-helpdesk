from typing import Union
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from simple_kanban.services.toast_service import ToastService
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
  """
    Generic Method to try and get a specific Model class by ID, from the database.
    Logs an error if not found.

    Params:
      request: Network Request
      model_class: A Static reference to a Model Class
      object_id: An ID to try and retrieve from the database.

    Returns:
      A Tuple of a boolean result and the Object or None
  """
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
  """
    Merges dictionaries.

    Duplicate keys will be overwritten.

    Params:
      N number of dictionary objects.
  """
  new_context = {}
  for obj in args:
    if isinstance(obj, dict):
      new_context.update(obj)
  return new_context

def redirect_with_toast(request, action: str, toast_header: str, message: str, *args):
  """
  Redirect to a named action (see simple_kanban/urls.py) action with a query parameter encoded message to the UI.
  
  The `args` are used for dynamic URL parameters, which will be passed to the reverse function.

  Typically used for redirecting a 404 error back to a page with a descriptive message. 
  """
  ToastService.send_toast_message(request, toast_header, message)
  
  redirect_url = reverse(action, args=args)
  
  return redirect(f"{redirect_url}")