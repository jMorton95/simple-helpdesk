def is_admin(user) -> bool:
  return user.groups.filter(name="Admin").exists()

def CreateUserContext(request, context):
  context["is_admin"] = is_admin(request.user)
  return context