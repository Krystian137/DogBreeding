from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import Dog, Litter

# Create your views here.
class DogList(ListView):
    model = Dog
    template_name = 'pets/dogs.html'
    context_object_name = 'dogs'
    paginate_by = 12

    def get_queryset(self):
        return Dog.objects.filter(
            show_in_list=True
        ).select_related('litter').prefetch_related('photos').order_by('-birth_date')


class DogProfile(DetailView):
    model = Dog
    template_name = 'pets/dog-profile.html'
    context_object_name = 'dog'

    def get_queryset(self):
        return Dog.objects.select_related(
            'litter',
            'mother',
            'father'
        ).prefetch_related('photos')


class LitterList(ListView):
    model = Litter
    template_name = 'pets/litters.html'
    context_object_name = 'litters'


class LitterDetails(DetailView):
    model = Litter
    template_name = 'pets/litter-details.html'
    context_object_name = 'litter'