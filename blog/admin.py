from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

