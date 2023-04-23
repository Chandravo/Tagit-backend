from django.db import models
from registration.models import User
from django.utils import timezone
# Create your models here.

class QR(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    qr = models.URLField(max_length=1000, null=False, blank=False)
    target = models.URLField(max_length=1000, null=False, blank=False, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='qr')
    key = models.CharField(max_length=50, unique=True, null=False, blank=False)
    def __str__(self):
        return self.user.email + '_' + self.name
    
class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr = models.ForeignKey(QR, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100,default='pending')
    product_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
    
class Scan(models.Model):
    qr=models.ForeignKey(QR, on_delete=models.CASCADE)
    location = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.time = timezone.localtime(timezone.now())
        super(Scan, self).save(*args, **kwargs)