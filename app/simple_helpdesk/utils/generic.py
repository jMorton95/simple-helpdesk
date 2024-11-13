from django.contrib import messages

def validate_form(request, form) -> bool:
  try:
   for _, errors in form.errors.items():
        for error in errors:
          messages.error(request, error)
   return form.is_valid()
  except:
    #TODO: Log Error
   return False