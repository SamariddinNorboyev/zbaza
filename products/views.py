import json
from argparse import Action

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
import openpyxl
from io import BytesIO
from products.forms import ProductForm
from products.models import Product, Actions
from django.contrib import messages
from django.http import HttpResponse


@login_required
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        amount = int(request.POST.get('amount'))
        product = Product.objects.filter(name=name, code=code).first()
        product.amount = product.amount - amount
        action = Actions(by_user=request.user, product=product, amount=amount)
        action.save()
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
        action = Actions(by_user=request.user, product=product, amount=amount)
        action.save()
        product.save()
        print(product)
        return redirect('products:add')
    products = Product.objects.all()
    products_data = list(products.values('code', 'name'))
    return render(request, 'products/add.html', {'products' :products, 'data': products_data, 'products_json': json.dumps(products_data)})



@login_required
def products(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('name')
            code = request.POST.get('code')
            amount = int(request.POST.get('amount'))
            price = request.POST.get('price')
            if Product.objects.filter(code=code).exists():
                messages.error(request, "Bu kod band! Iltimos boshqa kod tanlang.")
                return redirect('products:products')
            Product.objects.create(name=name, code=code, amount=amount, price=price)

        sort_by = request.GET.get('sort', '-updated_at')

        allowed_sort_fields = [
            'id', '-id',
            'name', '-name',
            'code', '-code',
            'price', '-price',
            'amount', '-amount',
            'updated_at', '-updated_at'
        ]

        if sort_by not in allowed_sort_fields:
            sort_by = '-updated_at'

        product_list = Product.objects.all().order_by(sort_by)

        paginator = Paginator(product_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        total_price = sum(i.total_price for i in page_obj)
        total_price = "{:,}".format(total_price).replace(",", " ")
        products_data = list(product_list.values('id', 'code', 'name'))

        return render(request, 'products/products.html', {
            'products': product_list,
            'page_obj': page_obj,
            'data': products_data,
            'products_json': json.dumps(products_data),
            'total_price': total_price,
            'current_sort': sort_by
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

    return render(request, 'products/edit.html', {'form': form, 'id': id})




@login_required
def export_products_excel(request):
    if request.user.is_superuser:
        products = Product.objects.all()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Products"

        # Add header
        ws.append(['ID', 'Name', 'Code', 'Amount', 'Total Price'])

        # Add data rows
        for product in products:
            ws.append([product.id, product.name, product.code, product.amount, product.total_price])

        # Save to BytesIO buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        # Return response
        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'
        return response

    return redirect('products:home')