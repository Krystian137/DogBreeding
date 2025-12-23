from django.shortcuts import render
from django.views.generic import ListView, TemplateView

# Create your views here.
class ReservationFormView(TemplateView):
    template_name = 'reservation/reservation.html'