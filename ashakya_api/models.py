from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Visitor(models.Model):
    ip_address = models.CharField(max_length=45,default='0.0.0.0')  # Supports IPv4 and IPv6
    user_agent = models.CharField(max_length=255,default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    country_name = models.CharField(max_length=100,default='Unknown')
    region_name = models.CharField(max_length=100,default='Unknown')
    zip_code = models.CharField(max_length=20,default='00000')
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.0)
    city = models.CharField(max_length=255, blank=True, null=True)
    referer = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"


