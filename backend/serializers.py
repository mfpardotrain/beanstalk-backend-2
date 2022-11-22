from rest_framework import serializers
from .models import FarmBoy, FarmVegetable, Order, Market, Farm, MarketInfo, FarmVegetableOrder


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmBoy
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'


class FarmVegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmVegetable
        fields = '__all__'


class FarmVegetableOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmVegetableOrder
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'


class MarketInfoSerializer(serializers.ModelSerializer):
    market = MarketSerializer(many=False, read_only=True)

    class Meta:
        model = MarketInfo
        fields = '__all__'


class MarketInfoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketInfo
        fields = '__all__'


class MarketVegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketInfo
        fields = '__all__'
        depth = 1
