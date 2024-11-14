from django.contrib import messages

def validate_form(request, form) -> bool:
  try:
    for _, errors in form.errors.items():
        for error in errors:
          messages.error(request, error)
    valid = form.is_valid()
    return valid
  except Exception as e:
    print(str(e))
  return False