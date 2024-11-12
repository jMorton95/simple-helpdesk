from .controllers import home_controller, auth_controller
from django.urls import path
 
urlpatterns = [
    path("", home_controller.index, name="index"),
    path("register", auth_controller.register, name="register"),
    path("login", auth_controller.login, name="login")
]
 