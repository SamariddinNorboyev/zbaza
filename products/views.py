from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from products.models import Product


@login_required
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        amount = int(request.POST.get('amount'))
        product = Product.objects.filter(name=name, code=code).first()
        product.amount = product.amount - amount
        product.save()
        print(product)
        return redirect('products:home')
    products = Product.objects.all()
    products_data = list(products.values('code', 'name'))
    return render(request, 'products/home.html', {'products' :products, 'data': products_data})



@login_required
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        amount = int(request.POST.get('amount'))
        product = Product.objects.filter(name=name, code=code).first()
        product.amount = product.amount + amount
        product.save()
        print(product)
        return redirect('products:add')
    products = Product.objects.all()
    products_data = list(products.values('code', 'name'))
    return render(request, 'products/add.html', {'products' :products, 'data': products_data})