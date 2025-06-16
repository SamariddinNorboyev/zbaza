from . import views
from django.urls import path, include

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add, name='add'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('products/', views.products, name='products'),
    path('export-excel/', views.export_products_excel, name='export_excel'),
]