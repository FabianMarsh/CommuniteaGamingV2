from django.contrib import admin
from .models import TeamMember, WhoWeAre

# Register your models here.

@admin.register(WhoWeAre)
class WhoWeAreAdmin(admin.ModelAdmin):
    list_display = ("text",)

    def has_add_permission(self, request):
        return not WhoWeAre.objects.exists()

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role")  # Shows name & role in the list
    search_fields = ("name", "role")  # Allows search by name & role
    list_filter = ("role",)  # Adds filtering option by role
    ordering = ("name",)  # Orders by name
    fieldsets = (
        (None, {"fields": ("name", "role", "bio", "photo")}),
    )
