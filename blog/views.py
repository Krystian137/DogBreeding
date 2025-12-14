from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import Post

# Create your views here.
class MainPageView(ListView):
    model = Post
    template_name = 'blog/main.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/main.html'
    context_object_name = 'post'
