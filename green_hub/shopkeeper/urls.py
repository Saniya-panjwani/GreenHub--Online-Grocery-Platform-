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
from django.urls import path,include
from .import views
app_name = "shopkeeper"
urlpatterns = [
   path('',views.dashboard,name='dashboard'),
   path('add-product/',views.add_product,name='add-product'),
   path('add-category/',views.add_category,name='add-category'),
   path('delete-category/<int:pk>',views.delete_category,name='delete-category'),
   path('view-product/',views.view_product,name='view-product'),
   path('manage-product/',views.manage_product,name='manage-product'),

   path('delete-product/<int:pk>/',views.delete_product,name='delete-product'),
   path('edit-product/<int:pk>/',views.edit_product,name='edit-product'),

   path('update-product/',views.update_product,name='update-product')

]
