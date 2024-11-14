from .views import helpdesk, auth
from django.urls import path
 
urlpatterns = [
    path("", helpdesk.index, name="index"),
    path("register", auth.register, name="register"),
    path("signin", auth.sign_in, name="sign_in"),
    path("signout", auth.sign_out, name="sign_out"),
    path("changepassword", auth.change_password, name="change_password")
]
 