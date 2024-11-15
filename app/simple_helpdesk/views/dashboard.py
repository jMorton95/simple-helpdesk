from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from simple_helpdesk.services.dashboard_service import DashboardService
from simple_helpdesk.models import Project

@login_required(login_url="/register")
def index(request):
  context = DashboardService.GetDashboardContext()
  
  return render(request, "helpdesk/dashboard.html", context)