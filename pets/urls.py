from django.urls import path
from . import views

app_name = 'zwierzaki'

urlpatterns = [
    path('lista/', views.DogList.as_view(), name='DogList'),
    path('mioty/', views.LitterList.as_view(), name='LitterList'),
    path('<slug:slug>/', views.DogProfile.as_view(), name='DogProfile'),
    path('mioty/<slug:slug>/', views.LitterDetails.as_view(), name='LitterDetails'),
]