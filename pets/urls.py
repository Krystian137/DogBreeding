from django.urls import path
from . import views

app_name = 'zwierzaki'

urlpatterns = [
    path('lista/', views.lista_psow.as_view(), name='lista'),

    path('<slug:slug>/', views.profil_psa.as_view(), name='profil_psa'),
]