from .views import auth, dashboard, project
from django.urls import path
 
urlpatterns = [
    path("", dashboard.index, name="index"),
    path("register", auth.register, name="register"),
    path("signin", auth.sign_in, name="sign_in"),
    path("signout", auth.sign_out, name="sign_out"),
    path("changepassword", auth.change_password, name="change_password"),
    path("project/create", dashboard.create_project, name="project_create"),
    path("project/edit/<int:project_id>", dashboard.edit_project, name="project_edit"),
    path("project/<int:project_id>/delete", dashboard.delete_project, name="project_delete"),
    path("project/<int:project_id>/swimlane/delete/<int:swimlane_id>", dashboard.delete_swimlane, name="swimlane_delete"),
    path("project/<int:project_id>", project.overview, name="project_overview"),
    path("project/<int:project_id>/ticket/create", project.create_ticket, name="ticket_create")
]