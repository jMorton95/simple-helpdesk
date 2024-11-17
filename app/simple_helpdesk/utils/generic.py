from django.contrib import messages

def form_is_valid(request, form) -> bool:
  try:
    if form.errors and form.errors.items() and len(form.errors.items()) > 0:
      for _, errors in form.errors.items():
          for error in errors:
            messages.error(request, error)
  except Exception as e:
    print(str(e))
  return form.is_valid()