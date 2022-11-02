from http.client import HTTPResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializers
from rest_framework import status
from .models import Category, Product
from rest_framework.permissions import IsAdminUser
from rest_framework import permissions


class CarrierAdminPermission(permissions.BasePermission):
    message = "Carrier Admin just allow ."

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_role == "CA":
            return True


class ProductView(APIView):
    permission_classes = [CarrierAdminPermission]

    # Retrieve Category
    def get(self, request, pk, format=None):
        data = Product.objects.get(pk=pk)
        serializer = ProductSerializers(data)
        return Response(serializer.data)

    # Create Instance for document
    def post(self, request, format=None):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
