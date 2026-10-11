from rest_framework import serializers
from .models import Category, Product, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'category_name', 'name', 'price', 'stock', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items', 'total', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if product.stock < quantity:
                order.delete()
                raise serializers.ValidationError(
                    f'Estoque insuficiente para "{product.name}". Disponível: {product.stock}'
                )

            product.stock -= quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price
            )

        return order