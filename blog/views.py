from django.core.paginator import Paginator
from django.shortcuts import render
from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.order_by('-created_at')
    paginator = Paginator(posts, 2)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})
