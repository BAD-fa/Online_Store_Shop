from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework import status

from Product.models import Product, Category, ProductComment
from .serializers import CategoryListSerializer, ProductSerializer, ProductListSerializer, ProductCommentSerializer,DiscountCodeSerializer
from .discount_code_sender import DiscountCodeRpcClient

rabit_MQ_sender = DiscountCodeRpcClient()

User = get_user_model()


class CategoryViewset(viewsets.ViewSet):

    def list(self, request):
        queryset = Category.objects.filter(cat__isnull=True)
        serializer = CategoryListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):

    @action(methods=['get'], detail=False)
    def product_list(self, request, name):
        queryset = Product.objects.filter(category__name=name)
        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, product_slug):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, product_slug=product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CommentAPI(ListCreateAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer

    def create(self, request, *args, **kwargs):
        comment = ProductCommentSerializer(data=request.data, context={'request': request})
        if comment.is_valid():
            comment.save()
            return Response(comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountCodeApi(ListCreateAPIView):

    def create(self, request):
        serializer_class = DiscountCodeSerializer(data=request.data)
        if serializer_class.is_valid():
            user_id_list = serializer_class.validated_data.get("user_id_list")
            day_expire_time = serializer_class.validated_data.get("day_expire_time")
            rabit_MQ_sender = DiscountCodeRpcClient()
            rabit_MQ_sender.call(user_id_list,day_expire_time)
            return rabit_MQ_sender.response
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)