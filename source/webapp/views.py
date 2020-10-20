from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductForm, SimpleSearchForm
from webapp.models import Product


class ProductListView(ListView):
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        data = Product.objects.all()
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return data

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None




# def index_view(request):
#     data = Product.objects.filter(amount__gt=0)
#     return render(request, 'index.html', context={
#         'products': data
#     })

class ProductView(DetailView):
    template_name = 'product_view.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# def product_view(request, pk):
#     product = get_object_or_404(Product,pk=pk)
#     context = {'product': product}
#     return render(request, 'product_view.html', context=context)


class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


# def product_create_view(request):
#     if request.method == 'GET':
#         form = ProductForm()
#         return render(request, 'product_create.html', context={
#             'form': form})
#     elif request.method == 'POST':
#         form = ProductForm(data=request.POST)
#         if form.is_valid():
#             product = Product.objects.create(**form.cleaned_data)
#             return redirect('product_view', pk=product.pk)
#         else:
#             return render(request, 'product_create.html', context={
#                 'form': form
#             })
#     else:
#         return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


# def product_update_view(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == "GET":
#         form = ProductForm(initial={
#             'name': product.name,
#             'description': product.description,
#             'amount': product.amount,
#             'category': product.category,
#             'price': product.price
#         })
#         return render(request, 'product_update.html', context={
#             'form': form,
#             'product': product
#         })
#     elif request.method == 'POST':
#         form = ProductForm(data=request.POST)
#         if form.is_valid():
#             product.name = form.cleaned_data['name']
#             product.description = form.cleaned_data['description']
#             product.amount = form.cleaned_data['amount']
#             product.category = form.cleaned_data['category']
#             product.price = form.cleaned_data['price']
#             product.save()
#             return redirect('product_view', pk=product.pk)
#         else:
#             return render(request, 'product_update.html', context={
#                 'product': product,
#                 'form': form
#             })
#     else:
#         return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


# def product_delete_view(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         return render(request, 'product_delete.html', context={'product': product})
#     elif request.method == 'POST':
#         product.delete()
#         return redirect('index')
#     else:
#         return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


class ProductDeleteView(DeleteView):
    template_name = 'product_delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('index')

# class BasketChangeView(StatsMixin, View):
#     def get(self, request, *args, **kwargs):
#         products = request.session.get('products', [])
#
#         pk = request.GET.get('pk')
#         action = request.GET.get('action')
#         next_url = request.GET.get('next', reverse('webapp:index'))
#
#         if action == 'add':
#             product = get_object_or_404(Product, pk=pk)
#             if product.in_order:
#                 products.append(pk)
#         else:
#             for product_pk in products:
#                 if product_pk == pk:
#                     products.remove(product_pk)
#                     break
#
#         request.session['products'] = products
#         request.session['products_count'] = len(products)
#
#         return redirect(next_url)
#
#
# class BasketView(StatsMixin, CreateView):
#     model = Order
#     form_class = BasketOrderCreateForm
#     template_name = 'product/basket.html'
#     success_url = reverse_lazy('webapp:index')
#
#     def get_context_data(self, **kwargs):
#         basket, basket_total = self._prepare_basket()
#         kwargs['basket'] = basket
#         kwargs['basket_total'] = basket_total
#         return super().get_context_data(**kwargs)
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#     def form_valid(self, form):
#         if self._basket_empty():
#             form.add_error(None, 'В корзине отсутствуют товары!')
#             return self.form_invalid(form)
#         response = super().form_valid(form)
#         self._save_order_products()
#         self._clean_basket()
#         messages.success(self.request, 'Заказ оформлен!')
#         return response
#
#     def _prepare_basket(self):
#         totals = self._get_totals()
#         basket = []
#         basket_total = 0
#         for pk, qty in totals.items():
#             product = Product.objects.get(pk=int(pk))
#             total = product.price * qty
#             basket_total += total
#             basket.append({'product': product, 'qty': qty, 'total': total})
#         return basket, basket_total
#
#     def _get_totals(self):
#         products = self.request.session.get('products', [])
#         totals = {}
#         for product_pk in products:
#             if product_pk not in totals:
#                 totals[product_pk] = 0
#             totals[product_pk] += 1
#         return totals
#
#     def _basket_empty(self):
#         products = self.request.session.get('products', [])
#         return len(products) == 0
#
#     def _save_order_products(self):
#         totals = self._get_totals()
#         for pk, qty in totals.items():
#             OrderProduct.objects.create(product_id=pk, order=self.object, amount=qty)
#
#     def _clean_basket(self):
#         if 'products' in self.request.session:
#             self.request.session.pop('products')
#         if 'products_count' in self.request.session:
#             self.request.session.pop('products_count')

