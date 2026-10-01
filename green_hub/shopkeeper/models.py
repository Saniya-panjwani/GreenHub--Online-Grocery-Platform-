from django.db import models
from data.models import*

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    category_description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name 
    

class Product(models.Model):
    Shopkeeper_fk = models.ForeignKey(Shopkeeper,on_delete=models.CASCADE)
    Category_fk = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30)
    sku = models.CharField(max_length=30)
    base_price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=5,decimal_places=2)
    stock_qty = models.PositiveIntegerField()
    UNIT_CHOICES = [
        ('Per Item','Per Item'),
        ('Per Kg' , 'Per Kg'),
        ('Per Liter' , 'Per Liter'),
        ('Per Pack' , 'Per Pack'),
        ('Per Box', 'Per Box'),
    ]
    unit = models.CharField(max_length=30,choices=UNIT_CHOICES,default='Per Item')
    description = models.TextField()
    images = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name
    
    def discount_price_value(self):
        return self.base_price - self.discount_price
    
    def low_stock_value(self):
        pass