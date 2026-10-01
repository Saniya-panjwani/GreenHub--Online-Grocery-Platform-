"""
URL configuration for green_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .import views

app_name="customer"
urlpatterns = [
    path('', views.home, name='home'),
    path('view-product/',views.view_product,name='view-product'),
    path('product-detail/<int:pk>',views.product_detail,name='product-detail'),

    path('add-to-cart/<int:pk>',views.add_to_cart,name='add-to-cart'),

    path('view-cart',views.view_cart,name='view-cart'),

    path("remove-cart-item/<int:id>/",views.remove_cart_item,name="remove_cart_item"),

    path('checkout/',views.checkout,name="checkout")

]
