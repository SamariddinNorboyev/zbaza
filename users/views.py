from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from .forms import LoginForm
from .models import MyUser


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = MyUser.objects.filter(username = username).first()
            login(request, user)
            return redirect('products:home')
        return render(request, 'users/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        if MyUser.objects.filter(username=username).exists():
            messages.error(request, "Bu username band! Iltimos boshqa username tanlang.")
            return redirect('users:register')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        is_master = request.POST.get('is_master') == 'on'
        user = MyUser(username=username, name=name, surname=surname, is_master=is_master)
        user.set_password(password)
        user.save()
        messages.success(request, "Foydalanuvchi yaratildi!")
        return redirect('users:users')
    return render(request, 'users/register.html',)


def users(request):
    if request.user.is_superuser:
        userlar = MyUser.objects.filter(is_superuser=False)
        print(userlar)
        return render(request, 'users/users.html', {'userlar': userlar})
    return redirect('products:home')


def makemaster(request, id):
    if request.user.is_superuser:
        user = MyUser.objects.get(id=id)
        user.is_master = not user.is_master
        user.save()
        return redirect('users:users')
    return redirect('products:home')


def makeactive(request, id):
    if request.user.is_superuser:
        user = MyUser.objects.get(id=id)
        user.is_active = not user.is_active
        user.save()
        return redirect('users:users')
    return redirect('products:home')