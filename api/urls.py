from django.urls import path
from .views import *
from rest_framework import routers
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
router = routers.DefaultRouter()
router = DefaultRouter()



router.register(r'vendors', Vendors, basename='vendors')
router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchase_orders')


urlpatterns = [
    path('', include(router.urls)),
]