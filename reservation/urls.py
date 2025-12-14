from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('rezerwuj/', views.RezerwacjaFormView.as_view(), name='rezerwacja'),
]