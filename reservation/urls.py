from django.urls import path
from . import views

app_name = 'rezerwacja'

urlpatterns = [
    path('', views.reservation_form_view, name='reservation-form'),
]