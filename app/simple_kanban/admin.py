from django.contrib import admin

from .models import Project, Ticket, Swimlane, TicketComment

#Exposes Data Models to DJango SUPERUSERS.
admin.site.register([Project, Ticket, Swimlane, TicketComment])