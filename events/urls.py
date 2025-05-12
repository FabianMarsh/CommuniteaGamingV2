from django.urls import path
from .views import events_view, add_event, edit_event, events_json, delete_event, is_admin

urlpatterns = [
    path("", events_view, name="events"),
    path("user/is_admin/", is_admin, name="is_admin"),
    path("json/", events_json, name="events_json"),
    path("edit/<int:event_id>/", edit_event, name="edit_event"),
    path("add/", add_event, name="add_event"),
    path("delete/<int:event_id>/", delete_event, name="delete_event"),
]

