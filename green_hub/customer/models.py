from django.db import models
from data.models import*
from shopkeeper.models import *
# Create your models here.

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=30,unique=True)
    discount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)


class Cart(models.Model):
    customer_fk = models.ForeignKey(Customer,on_delete=models.CASCADE)
    coupon_fk = models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cart - {self.customer_fk.first_name}"


class CartItem(models.Model):
    cart_fk = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.cart_fk.customer_fk.first_name} : {self.product_fk.product_name} : ({self.qty})"
    
    def total_item_price(self):
        return self.price*self.qty

class OrderRecord(models.Model):
    PAYMENT_METHOD = [
        ('razorpay',"Razorpay"),
        ('cod','Cash On Delivery')
    ]
    PAYMENT_STATUS = [
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','Failed')
    ]

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=40)
    mobile_no = models.CharField(max_length=12)
    address = models.TextField()
    city = models.CharField(max_length=30)
    pincode = models.CharField(max_length=8)
    delivery_note = models.TextField(
        blank=True,
        null=True,
        help_text="Special delivery instructions"
    )
    payment_method = models.CharField(max_length=12,choices=PAYMENT_METHOD,default="cod")
    payment_status = models.CharField(max_length=12,choices=PAYMENT_STATUS,default="pending")
    

    created_at = models.DateTimeField(auto_now_add=True)

