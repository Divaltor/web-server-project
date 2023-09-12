from rest_framework import serializers

from server.models import Item, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = fields


class ItemSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True, many=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        many=True
    )

    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'description', 'buy_price', 'sell_price', 'image', 'quantity', 'category', 'category_id']
        read_only_fields = fields
        extra_kwargs = {
            'name': {'max_length': 50},
            'description': {'max_length': 2000},
        }
