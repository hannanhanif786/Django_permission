from .models import Product
from rest_framework import serializers


# contact serializer class
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
