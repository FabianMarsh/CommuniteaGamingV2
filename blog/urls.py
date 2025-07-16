from django.urls import path
from .views import blog_list

app_name = "blog"

urlpatterns = [
    path("", blog_list, name="blog"),
]