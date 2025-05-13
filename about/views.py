from django.shortcuts import render

from .models import TeamMember, WhoWeAre

def about_view(request):
    who_we_are = WhoWeAre.objects.first()  # Get the first (and only) entry
    team = TeamMember.objects.all()
    return render(request, "about/about.html", {"who_we_are": who_we_are, "team": team})

