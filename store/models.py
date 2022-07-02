import email
from itertools import product
from statistics import mode
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LikedItem(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey()

class Tag(models.Model):
    label=models.CharField(max_length=255)

class TaggedItem(models.Model):
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey()

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount=models.FloatField()

class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')

class Product(models.Model):
    title = models.CharField(max_length=255) #varchar(255)
    slug=models.SlugField()
    description = models.TextField() #9999.99
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions=models.ManyToManyField(Promotion)

class Customer (models.Model):
    MEMBERSHIP_BRONZE="B"
    MEMBERSHIP_SILVER="S"
    MEMBERSHIP_GOLD="G"

    MEMBERSHIP_CHOICES=[(MEMBERSHIP_BRONZE,"Bronze"),(MEMBERSHIP_SILVER,"Silver"),(MEMBERSHIP_GOLD,"Gold"),]
    first_name = models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date= models.DateField(null=True)
    membership = models.CharField(max_length=1 , choicess=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
class Order (models.Model):
    PAYEMENT_STATUS_PENDING="P"
    PAYEMENT_STATUS_COMPLETE="C"
    PAYEMENT_STATUS_FAILED="F"
    PAYEMENT_STATUS_CHOICES=[(PAYEMENT_STATUS_PENDING,"Pending"),(PAYEMENT_STATUS_COMPLETE,"Complete"),(PAYEMENT_STATUS_FAILED,"Failed")]
    placed_at = models.DateTimeField(auto_now_add=True),
    payement_status= models.CharField(max_length=1,choices=PAYEMENT_STATUS_CHOICES,default=PAYEMENT_STATUS_PENDING)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)

class Adress(models.Model):
    street=models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE) #on_delete=models.CASCADE (when customer is deleted the adress is also deleted)

class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField()