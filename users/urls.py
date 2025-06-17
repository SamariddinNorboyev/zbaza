from . import views
from django.urls import path


app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('users/', views.users, name='users'),
    path('makemaster/<int:id>', views.makemaster, name='makemaster'),
    path('makeactive/<int:id>', views.makeactive, name='makeactive'),
]