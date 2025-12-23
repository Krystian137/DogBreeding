from django.urls import path
from . import views

app_name = 'rezerwacja'

urlpatterns = [
    path('rezerwacja/', views.ReservationFormView.as_view(), name='reservation-form'),
]