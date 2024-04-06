from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import F, Count, Case, When
from django.dispatch import receiver
from django.db.models.signals import post_save

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(null = True, blank = True)
    quality_rating_avg = models.FloatField(null = True, blank = True)
    average_response_time = models.FloatField(null = True, blank = True)
    fulfillment_rate = models.FloatField(null = True, blank = True)

    def __str__(self):
        return self.name

    

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'cancelled'),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    order_date = models.DateTimeField(null = True, blank = True,auto_now_add=True)
    delivery_date = models.DateTimeField(null = True, blank = True)
    # items =  models.JSONField(null = True, blank = True)
    items =  models.TextField(null = True, blank = True)
    quantity = models.IntegerField(null = True, blank = True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank = True)
    issue_date = models.DateTimeField(null = True, blank = True,auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return self.po_number
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            last_po = PurchaseOrder.objects.last()
            if last_po:
                last_number = int(last_po.po_number)
                new_number = last_number + 1
                self.po_number = str(new_number)
            else:
                self.po_number = "1" 
        super().save(*args, **kwargs)


@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        on_time_count = vendor.purchaseorder_set.filter(status='completed', delivery_date__lte=F('promised_delivery_date')).count()
        total_completed_count = vendor.purchaseorder_set.filter(status='completed').count()
        on_time_delivery_rate = (on_time_count / total_completed_count) * 100 if total_completed_count > 0 else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        quality_rating_avg = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False).aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date is not None:
        vendor = instance.vendor
        response_times = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False).annotate(response_time=F('acknowledgment_date') - F('issue_date')).values_list('response_time', flat=True)
        average_response_time = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
        vendor.average_response_time = average_response_time
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, created, **kwargs):
    vendor = instance.vendor
    fulfilled_count = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=True).count()
    total_count = vendor.purchaseorder_set.count()
    fulfillment_rate = (fulfilled_count / total_count) * 100 if total_count > 0 else 0
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(null = True, blank = True)
    quality_rating_avg = models.FloatField(null = True, blank = True)
    average_response_time = models.FloatField(null = True, blank = True)
    fulfillment_rate = models.FloatField(null = True, blank = True)

    def __str__(self):
        return f"{self.vendor} - {self.date}"


