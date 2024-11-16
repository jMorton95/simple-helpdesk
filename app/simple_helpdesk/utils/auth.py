def is_admin(user) -> bool:
  return user.groups.filter(name="Admin").exists()