from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import Dog, Litter

# Create your views here.
class DogList(ListView):
    model = Dog
    template_name = 'pets/dogs.html'
    context_object_name = 'dogs'


class DogProfile(DetailView):
    model = Dog
    template_name = 'pets/dog-profile.html'
    context_object_name = 'dog-profile'


class LitterList(ListView):
    model = Litter
    template_name = 'pets/litters.html'
    context_object_name = 'litters'


class LitterDetails(DetailView):
    model = Litter
    template_name = 'blog/litter-details.html'
    context_object_name = 'litter-details'