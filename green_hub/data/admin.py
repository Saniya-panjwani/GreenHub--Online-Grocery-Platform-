from django.contrib import admin
from .models import *
# Register your models here.



class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','role','created_at']
    list_display_links = ['id']
    search_fields = ['email']
    list_filter = ['role','created_at']
    list_per_page = 10

class ShopkeeperAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','shop_name']
    list_display_links = ['first_name']
    search_fields = ['shop_name','first_name']
    list_filter = ['first_name','last_name']
    list_per_page = 10

admin.site.register(User,UserAdmin)
admin.site.register(Shopkeeper,ShopkeeperAdmin)