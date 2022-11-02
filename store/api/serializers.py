from rest_framework import serializers
from store.models import Item, OrderItem, Order
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer
    user = UserSerializer
    user_name = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('user_name', 'user', 'ordered', 'item_name', 'item', 'quantity')

    def get_item_name(self, obj):
        return obj.item.title

    def get_user_name(self, obj):
        return obj.user.username


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer
    items = OrderItemSerializer
    item_names = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('user', 'item_names', 'items', 'ordered', 'ordered_date', 'address')

    def get_item_names(self, obj):
        query = obj.items.all()
        item = []
        for i in query:
            item.append(i.item.title)
        return item
