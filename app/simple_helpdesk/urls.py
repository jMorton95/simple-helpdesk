from .views import helpdesk, auth
from django.urls import path
 
urlpatterns = [
    path("", helpdesk.index, name="index"),
    path("register", auth.register, name="register"),
    path("login", auth.login, name="login")
]
 