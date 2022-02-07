import json

from django.shortcuts import redirect

from Product.models import Product

from rest_framework import serializers


from Product.utils import add_to_cart

class CartSerializer(serializers.Serializer):
    
    cart_items = serializers.DictField()



    def add_to_cart_api(self):
        cart_items = self.validated_data.get("cart_items")
        products = Product.objects.filter(id__in=cart_items.keys())
        mapping = {}
        for elm in products:
            detail = [elm.price,elm.img.url,cart_items[str(elm.id)],elm.product_slug]
            mapping[elm.name]=json.dumps(detail)
        add_to_cart(self.request,mapping)
        return redirect("api:payment_api:cart_api")


    def __init__(self, request,instance=None, data=..., **kwargs):
        self.request = request
        super().__init__(instance, data, **kwargs)