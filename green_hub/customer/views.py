from django.shortcuts import render,get_object_or_404,redirect
from data.models import*
from shopkeeper.models import*
from .models import *
from django.db.models import Q
from data.views import*
from django.shortcuts import HttpResponse
from razorpay import Client
# Create your views here.

def home(request):
    all_products = Product.objects.all()
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "customer":
            cid = Customer.objects.get()
            context = {
                'uid' : uid,
                'cid' : cid,
                'all_products' : all_products
            }
            return render(request,"customer/index.html",context)
    context = {
        'all_products' : all_products
    }
    return render(request,"customer/index.html",context)

def view_product(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()
    Search = request.GET.get("search")
   
    if Search:
        all_products = all_products.filter(
            Q(product_name__icontains = Search) |

            Q(description__icontains = Search)
        )

    selected_category = request.GET.getlist("category_choice")
    if selected_category:
        all_products = all_products.filter(
            Q(Category_fk__id__in = selected_category)
        )

    #radio filter
    price = request.GET.get("price")

    if price == "100":
        all_products = all_products.filter(base_price__lt = 100)
    elif price == "500":
        all_products = all_products.filter(base_price__gte = 101,base_price__lt = 500)
    elif price == "501":
        all_products =all_products.filter(base_price__gte = 501)

    #sort - filter
    sort_value = request.GET.get("sort")

    if sort_value == "low":
        all_products = all_products.all().order_by("base_price")
    elif sort_value == "high":
        all_products = all_products.all().order_by("-base_price")
    elif sort_value == "new":
        all_products = all_products.all().order_by("-created_at")


    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "customer":
            cid = Customer.objects.get()
            context = {
                'uid' : uid,
                'cid' : cid,
                'all_products' : all_products,
                'selected_category' : selected_category,
                'categories': categories,
                'price' : price
            }
            return render(request,"customer/view-product.html",context)
    context = {
        'all_products' : all_products,
        'selected_category' : selected_category,
        'categories': categories,
        'price' : price

    }
    return render(request,"customer/view-product.html",context)

def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)

    context = {
        'product' : product
    }

    return render(request,"customer/product-detail.html",context)

@checkLogin
def add_to_cart(request,pk):
    uid = request.uid
    product = Product.objects.get(id = pk)
    customer = Customer.objects.get(user_fk = uid)

    cart,created = Cart.objects.get_or_create(customer_fk = customer)

    cartItem = CartItem.objects.filter(cart_fk = cart,product_fk = product).first()

    discounted_price = product.base_price - product.discount_price

    if cartItem:
        cartItem.qty += 1
        cartItem.save()

    else:
        CartItem.objects.create(cart_fk = cart,
                                product_fk = product,
                                qty = 1,
                                price = discounted_price
                                )

    return redirect("customer:view-cart")

@checkLogin
def view_cart(request):
    uid = request.uid

    customer_fk = Customer.objects.get(user_fk = uid)
    cart = Cart.objects.get(customer_fk = customer_fk)

    cart_items = CartItem.objects.filter(cart_fk = cart)
    cart_items_count = CartItem.objects.filter(cart_fk = cart).count()

    total_price = 0
    discount =0
    net_price = 0
    for item in cart_items:
        total_price +=  item.qty*item.price

    net_price = total_price
    if total_price >= 500 :
        discount = 65
        net_price -= discount

    context = {
        'uid' : uid,
        'cart_items' : cart_items,
        'cart_items_count' : cart_items_count,
        'total_price' : total_price,
        'discount' : discount,
        'net_price' : net_price,
        'cid' : customer_fk

    }
    return render(request,"customer/view_cart.html",context)

@checkLogin
def remove_cart_item(request,id):
    cart_item = get_object_or_404(CartItem,id=id)

    cart_item.delete()

    return redirect("customer:view-cart")

@checkLogin
def checkout(request):
    uid = request.uid
    customer_fk = Customer.objects.get(user_fk = uid)
    cart = Cart.objects.get(customer_fk = customer_fk)  
    cart_items = CartItem.objects.filter(cart_fk = cart)

    total_price = 0
    discount =0
    net_price = 0
    
    for item in cart_items:
        total_price +=  item.qty*item.price
    
    net_price = total_price
    if total_price >= 500 :
        discount = 65
        net_price -= discount

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name =  request.POST['last_name']
        email =  request.POST['email']
        mobile_no =  request.POST['mobile_no']
        address =  request.POST['address']
        city =  request.POST['city']
        pincode =  request.POST['pincode']
        delivery_note =  request.POST['delivery_note']

        payment_method =  request.POST['payment_method']

        if payment_method == "razorpay":
            client = Client.objects.create()
            return HttpResponse("process to payment gateway")
        elif payment_method == "cod":
            pass 

    
    context = {
        'uid' : uid,
        'cid' : customer_fk,
        'cart' :cart,
        'cart_items' : cart_items,
        'total_price' : total_price,
        'discount' : discount,
        'net_price' : net_price,
        # 'saved_addresses' : saved_addresses,
        # 'show_address_form' : show_address_form
    }
    return render(request,"customer/checkout.html",context)