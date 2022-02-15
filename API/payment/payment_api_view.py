from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .Serializer import CartSerializer
from Product.utils import redis_client_config,dict_decoder

class CartApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if request.user.is_authenticated:
            cart_data = dict_decoder(redis_client_config().hgetall(request.user.email))
        else:
            cart_data = dict_decoder(redis_client_config().hgetall(request.session.session_key))

        return Response(cart_data)

    def post(self,request):
        cart_serializer = CartSerializer(request,data=request.data)
        if cart_serializer.is_valid():
            return cart_serializer.add_to_cart_api()
        else:
            return Response(CartSerializer.data,status=status.HTTP_400_BAD_REQUEST)