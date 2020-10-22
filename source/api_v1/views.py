from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from api_v1.permissions import CheckIsStaff,  GETModelPermissions
from api_v1.serializers import ProductSerializer, OrderSerializer, OrderProductSerializer
from webapp.models import Product, Order, Cart
from django.shortcuts import get_object_or_404


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    permission_classes = [CheckIsStaff]

    def list(self, request):
        objects = Product.objects.all()
        slr = ProductSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = ProductSerializer(data=request.data, context={'request': request})
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(product, context={'request': request})
        return Response(slr.data)

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(data=request.data, instance=product, context={'request': request})
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'pk': pk})


class OrderViewSet(ViewSet):
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # self.request.method == "GET"
            return [GETModelPermissions()]
        else:
            return [AllowAny()]

    def list(self, request):
        objects = Order.objects.all()
        slr = OrderSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)


    def create(self, request):
        # order_products = request.data.pop('order_product')
        # print(order_products[0])
        # print(type(order_products[0]))
        print(request.data)
        slr = OrderSerializer(data=request.data, context={'request': request})

        if slr.is_valid():
            order = slr.save()
            cart_ids = self.request.session.get('cart_ids', [])
            order_products =[]
            for i in cart_ids:
                print(i)
                cart = get_object_or_404(Cart, pk= i)
                order_product = OrderProductSerializer(data={'product': cart.product.pk, 'order':order.pk, 'qty': cart.qty })
                cart.delete()
                if order_product.is_valid():
                    order_save = order_product.save()
                    order_products.append(order_product)
            print(order_products)
            self.request.session.pop('cart_ids')
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)



    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        slr = OrderSerializer(order, context={'request': request})
        return Response(slr.data)


