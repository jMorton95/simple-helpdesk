from typing import List, Union
from django.contrib import messages

def form_is_valid(request, form) -> bool:
  try:
    if form.errors and form.errors.items and len(form.errors.items()) > 0:
      for _, errors in form.errors.items():
          for error in errors:
            messages.error(request, error)
  except Exception as e:
    print(str(e))
  return form.is_valid()

def get_object_if_exists(model_class, object_id) -> Union[bool, object | None]:
  try:
      obj = model_class.objects.get(pk=object_id)
      return [True, obj]
  except model_class.DoesNotExist:
      return [False, None]
    
def merge_contexts(*args) -> dict:
  new_context = {}
  for obj in args:
    if isinstance(obj, dict):
      new_context.update(obj)
  return new_context