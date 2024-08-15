from rest_framework import serializers
from .models import Product, Stock, StockProduct
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    print('Hello')
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']
    pass


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
    pass


class StockSerializer(serializers.ModelSerializer):

    positions = ProductPositionSerializer(many=True)
    
    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            price = Decimal(position['price'])
            StockProduct.objects.update_or_create(
                defaults={
                'stock': stock, 
                "product": position.get('product'), 
                "quantity": position.get('quantity'),   
                "price": price
                }, 
                stock=stock, 
                product=position['product'])
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            price = Decimal(position['price'])
            StockProduct.objects.update_or_create(
                defaults={
                'stock': stock, 
                "product": position.get('product'), 
                "quantity": position.get('quantity'),
                "price": price
                }, 
                stock=stock, 
                product=position['product'])
        return stock

    
    class Meta:
        model = Stock
        fields = ['address', 'positions']
    
