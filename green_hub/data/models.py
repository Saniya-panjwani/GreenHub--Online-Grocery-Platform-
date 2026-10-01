from django.db import models

# Create your models here.
class User(models.Model):
    ROLE_CHOICE =[
        ('shopkeeper','Shopkeeper'),
        ('customer','Customer')
    ]
    email = models.EmailField(max_length=30,unique=True)
    password = models.CharField(max_length=30)
    otp = models.PositiveIntegerField(default = 456)
    role = models.CharField(max_length=12,choices=ROLE_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)

class Shopkeeper(models.Model):
    user_fk = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 
    shop_name = models.CharField(max_length=60,blank=True,null=True)
    contact_no = models.PositiveIntegerField(blank=True,null=True)
    image = models.ImageField(upload_to='data_images/',default="defaultPic.png")
    address = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    user_fk = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_no = models.PositiveIntegerField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)