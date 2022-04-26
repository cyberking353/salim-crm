from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150, null=True)
    profile_pic = models.ImageField(null=True, default='salim2.png',blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Tags(models.Model):
    name = models.CharField(max_length=150,null=True)
    def __str__(self):
        return self.name[:]



class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Out Door','Out Door'),
        
    )
    name = models.CharField(max_length=150, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=150, null=True, choices = CATEGORY)
    description = models.CharField(max_length=150, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
       return self.name[:]




  

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    STATUS = (
        ('Pending','Pending'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=150, null=True, choices=STATUS)
    
    def __str__(self):
       return self.product.name