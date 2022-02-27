from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status



from Product.models import Product, Category, ProductComment, ProductDetails, ProductImage

User = get_user_model()


class SubCatHyperlink(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:api_product:list', 'lookup_field': 'name'}
        }


class SubCategorySerializer(serializers.ModelSerializer):
    sub_cat = SubCatHyperlink(many=True)

    class Meta:
        model = Category
        fields = ['name', 'sub_cat']


class CategoryListSerializer(serializers.ModelSerializer):
    sub_cat = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'sub_cat']


class ProductCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductComment
        fields = ['date', 'content', 'rate', 'author', 'product']

    def create(self, validated_data):
        obj = super().create(validated_data)
        email = self.context['request'].user.email
        user = get_object_or_404(User, email=email)
        obj.author = user
        obj.save()
        return obj


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDetails
        fields = ['property', 'detail']


class ProductSerializer(serializers.ModelSerializer):
    comments = ProductCommentSerializer(many=True)
    details = ProductDetailSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'rate', 'details', 'comments']


class ProductListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ['url', 'name', 'price', 'rate']
        extra_kwargs = {
            'url': {'view_name': 'api:api_product:detail', 'lookup_field': 'product_slug'}
        }


class DiscountCodeSerializer(serializers.Serializer):
    user_id_list = serializers.ListField()
    day_expire_time = serializers.IntegerField()