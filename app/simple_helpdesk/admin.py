from django.contrib import admin

from .models import Project, Ticket, Swimlane, TicketComment

admin.site.register([Project, Ticket, Swimlane, TicketComment])