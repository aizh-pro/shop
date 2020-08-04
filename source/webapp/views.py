from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import ProductForm
from webapp.models import Product


def index_view(request):
    data = Product.objects.all()
    return render(request, 'index.html', context={
        'products': data
    })


def product_view(request, pk):
    product = get_object_or_404(Product,pk=pk)
    context = {'product': product}
    return render(request, 'product_view.html', context=context)


def product_create_view(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product_create.html', context={
            'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(**form.cleaned_data)
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_create.html', context={
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])