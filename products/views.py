import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from products.forms import ProductForm
from products.models import Product
from django.contrib import messages


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
    return render(request, 'products/home.html', {'products' :products, 'data': products_data, 'products_json': json.dumps(products_data)})



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



@login_required
def products(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('name')
            code = request.POST.get('code')
            amount = int(request.POST.get('amount'))
            if Product.objects.filter(code=code).exists():
                messages.error(request, "Bu kod band! Iltimos boshqa kod tanlang.")
                return redirect('products:products')
            Product.objects.create(name=name, code=code, amount=amount)

        product_list = Product.objects.all().order_by('-id')  # full list
        paginator = Paginator(product_list, 10)  # paginate it
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        products_data = list(product_list.values('code', 'name'))

        return render(request, 'products/products.html', {
            'products': product_list,
            'page_obj': page_obj,
            'data': products_data
        })

    return redirect('products:home')



@login_required
def delete(request, id):
    if request.user.is_superuser:
        products = Product.objects.get(id=id)
        products.delete()
        return redirect('products:products')
    return redirect('products:home')



@login_required
def edit(request, id):
    if not request.user.is_superuser:
        return redirect('products:home')

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            code = form.cleaned_data['code']
            if Product.objects.filter(code=code).exclude(id=product.id).exists():
                messages.error(request, "Bu kod band! Iltimos boshqa kod tanlang.")
            else:
                form.save()
                messages.success(request, "Mahsulot muvaffaqiyatli yangilandi.")
                return redirect('products:products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit.html', {'form': form})