from .views import auth, helpdesk
from django.urls import path
 
urlpatterns = [
    path("", helpdesk.index, name="index"),
    path("register", auth.register, name="register"),
    path("signin", auth.sign_in, name="sign_in"),
    path("signout", auth.sign_out, name="sign_out"),
    path("changepassword", auth.change_password, name="change_password"),
    path("project/create", helpdesk.create_project, name="project_create"),
    path("project/edit/<int:project_id>", helpdesk.edit_project, name="project_edit"),
    path("project/<int:project_id>/swimlane/delete/<int:swimlane_id>", helpdesk.delete_swimlane, name="swimlane_delete")
]
 