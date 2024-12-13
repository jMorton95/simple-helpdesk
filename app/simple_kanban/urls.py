from .views import auth, dashboard, project
from django.urls import path
 
"""
  Specifies all endpoints used throughout the application.
  First arg is the URL path, <int:id> indicates a dynamic route.
  Second arg points an endpoint to a Controller/View action.
  Third arg aliases the endpoint name for use throughout Views/Templates
"""

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
    path("project/<int:project_id>/ticket/new", project.create_ticket_form, name="ticket_new"),
    path("project/<int:project_id>/ticket/create", project.create_ticket, name="ticket_create"),
    path("project/<int:project_id>/<int:ticket_id>/view", project.edit_ticket_form, name="ticket_view"),
    path("project/<int:project_id>/<int:ticket_id>/edit", project.edit_ticket, name="ticket_edit"),
    path("project/<int:project_id>/<int:ticket_id>/comment", project.add_comment, name="comment_create"),
    path("project/<int:project_id>/<int:ticket_id>/<int:ticketcomment_id>/edit", project.edit_comment, "comment_edit"),
    path("project/<int:project_id>/<int:ticket_id>/<int:ticketcomment_id>/delete", project.delete_comment, name="comment_delete"),
    path("project/<int:project_id>/<int:ticket_id>/delete", project.delete_ticket, name="ticket_delete")
]