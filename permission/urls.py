from django.urls import path
from .views import ProductView

urlpatterns = [path("product/<pk>", ProductView.as_view())]
