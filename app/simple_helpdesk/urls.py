from .views import dashboard, auth
from django.urls import path
 
urlpatterns = [
    path("", dashboard.index, name="index"),
    path("register", auth.register, name="register"),
    path("signin", auth.sign_in, name="sign_in"),
    path("signout", auth.sign_out, name="sign_out"),
    path("changepassword", auth.change_password, name="change_password")
]
 