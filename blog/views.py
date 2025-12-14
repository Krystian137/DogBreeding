from django.shortcuts import render
from django.views.generic import ListView, TemplateView

# Create your views here.
class MainPageView(TemplateView):
    template_name = 'blog/main.html'


class PostDetailsView(TemplateView):
    template_name = 'blog/main.html'
