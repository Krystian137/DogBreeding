from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
]