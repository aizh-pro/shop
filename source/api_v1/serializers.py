from rest_framework import serializers
from webapp.models import Product, Order, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'amount', 'price']


class OrderProductSerializer(serializers.ModelSerializer):
    # order = serializers.PrimaryKeyRelatedField(required=False)
    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'order', 'qty']

# class OrderProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     product = serializers.PrimaryKeyRelatedField(read_only=True)
#     order = serializers.PrimaryKeyRelatedField(read_only=True)
#     qty = serializers.IntegerField(read_only=True)
#
#     def create(self, validated_data):
#         return OrderProduct.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance


class OrderSerializer(serializers.ModelSerializer):
    order_product = OrderProductSerializer(many=True, source='order_products', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'name', 'phone', 'address', 'created_at', 'order_product']




