from . import views
from django.urls import path, include

app_name = 'products'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('add/', views.add, name='add'),
]