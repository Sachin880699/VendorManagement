from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from vendor.models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework import viewsets, status, permissions



class Vendors(viewsets.ViewSet):
    def list(self, request):
        vendor_list = Vendor.objects.all().order_by("id")
        context = {
            "Message": "success",
            "Output": VendorSerializer(vendor_list, many=True, context={'request': request}).data,
        }
        return Response(context)

    def create(self, request):
        data = request.data
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            vendor_id = data.get('id')
            serializer.save(id=vendor_id)
            return Response({
                "Message": "Created successfully",
                "Output": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            vendor = Vendor.objects.get(pk=kwargs.get('pk'))
            serializer = VendorSerializer(vendor)
            return Response({
                "Message": "Retrieved successfully",
                "Output": serializer.data
            })
        except Vendor.DoesNotExist:
            return Response({"Message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(instance=vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "Message": "Updated successfully",
                    "Output": serializer.data
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({"Message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            vendor.delete()
            return Response({"Message": "Deleted successfully"})
        except Vendor.DoesNotExist:
            return Response({"Message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
   
    
class PurchaseOrderViewSet(viewsets.ViewSet):
    def create(self, request, format=None):
        vendor_id = request.data.get('vendor_id')
        vendor_obj = Vendor.objects.get(id=vendor_id)
        items = request.data.get('items')
        quantity = request.data.get('quantity')
        status = request.data.get('status')
        
        purchase_order_obj = PurchaseOrder.objects.create(
            vendor=vendor_obj,
            items=items,
            quantity=quantity,
            status=status,   
        )
        return Response({
            "Message": "Created successfully",
            "Output": PurchaseOrderSerializer(purchase_order_obj, many=False, context={'request': request}).data,
        })

    def list(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            purchase_orders = purchase_orders.filter(vendor_id=vendor_id)
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=pk)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response({"Message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            vendor_id = request.data.get('vendor_id')
            vendor_obj = Vendor.objects.get(id=vendor_id)
            items = request.data.get('items')
            quantity = request.data.get('quantity')
            status = request.data.get('status')
            delivery_date = request.data.get('delivery_date')
            
            purchase_order_obj = PurchaseOrder.objects.filter(po_number = pk).update(
                vendor=vendor_obj,
                items=items,
                quantity=quantity,
                status=status,
                delivery_date = delivery_date,
                quality_rating = quality_rating
            )
            return Response({
                "Message": "Retrieved successfully",
                "Output": PurchaseOrderSerializer(purchase_order_obj, many=False, context={'request': request}).data,
            })
        except PurchaseOrder.DoesNotExist:
            return Response({"Message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=pk)
            purchase_order.delete()
            return Response({"Message": "Purchase order deleted successfully"})
        except PurchaseOrder.DoesNotExist:
            return Response({"Message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
