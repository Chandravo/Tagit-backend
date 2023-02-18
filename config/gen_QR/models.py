from django.db import models
from registration.models import User

# Create your models here.

class QR(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    qr = models.URLField(max_length=1000, null=False, blank=False)
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

    def __str__(self):
        return self.order_id
    
class scan(models.Model):
    qr=models.ForeignKey(QR, on_delete=models.CASCADE)
    location = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)