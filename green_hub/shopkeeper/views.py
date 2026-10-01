from django.shortcuts import render
from data.models import*
from data.views import*
from .models import*
from django.db.models import Q


# Create your views here.
@checkLogin
def dashboard(request):
    uid = request.uid
    sid = Shopkeeper.objects.get(user_fk =uid)
    context={
        'uid' : uid,
        'sid' : sid,
    }
    return render(request,"shopkeeper/seller-dashboard.html",context)

@checkLogin
def add_category(request):
    uid = request.uid
    sid = Shopkeeper.objects.get(user_fk = uid)
    if request.POST:
        category_name = request.POST['category_name']
        category_description = request.POST['category_description']

        Category.objects.create(category_name = category_name,
                                category_description = category_description)
    # fecht categories
    categories = Category.objects.all()
    context = {
        'uid' : uid,
        'sid' : sid,
        'categories' : categories
    } 
    return render(request,"shopkeeper/seller-add-category.html",context)

@checkLogin
def add_product(request):
    uid = request.uid
    sid = Shopkeeper.objects.get(user_fk =uid)
    Categories = Category.objects.all()
    
    if request.POST:
        product_name = request.POST['product_name']
        sku = request.POST['sku']
        category = request.POST['category']
        base_price = request.POST['base_price']
        discount_price = request.POST['discount_price']
        stock_qty = request.POST['stock_qty']
        unit = request.POST['unit']
        description = request.POST['description']
        images = request.FILES['images']

        cate_id = Category.objects.get(id = category)

        Product.objects.create(
            Shopkeeper_fk = sid,
            Category_fk = cate_id,
            product_name = product_name,
            sku = sku,
            base_price = base_price,
            discount_price = discount_price,
            stock_qty = stock_qty,
            unit = unit,
            description = description,
            images = images
        )
        return redirect("shopkeeper:view-product")
    context={
        'uid' : uid,
        'sid' : sid,
        'categories' : Categories,
        'unit_choice' : Product.UNIT_CHOICES
    }
    return render(request,"shopkeeper/seller-add-product.html",context)

@checkLogin
def delete_category(request,pk):
    uid = request.uid
    sid = Shopkeeper.objects.get(user_fk =uid)
    categories = Category.objects.all()

    category_id = Category.objects.get(id=pk)
    category_id.delete()
    
    return redirect("shopkeeper:add-category")

@checkLogin
def view_product(request):
    uid = request.uid
    sid = Shopkeeper.objects.get(user_fk =uid)

    my_products_all =Product.objects.filter(Shopkeeper_fk = sid)

    context = {
        'uid' : uid,
        'sid' : sid,
        'my_products_all' : my_products_all
    }

    return render(request,"shopkeeper/seller-view-products.html",context)

@checkLogin
def manage_product(request):
    
    uid = request.uid
    sid = Shopkeeper.objects.get(user_fk =uid)
    my_products_all =Product.objects.filter(Shopkeeper_fk = sid)
    category_all = Category.objects.all()

    print("hello")

    Search = request.GET.get("search")
    
    if Search:
        my_products_all = my_products_all.filter(
            Q(product_name__icontains = Search) |

            Q(description__icontains = Search)
        )

    category_name = request.GET.get("category_name")

        
    if category_name:
        my_products_all = my_products_all.filter(Category_fk__category_name = category_name)
    
    

    context = {
        'uid' : uid,
        'sid' : sid,
        'my_products_all' : my_products_all,
        'category_all' : category_all
    }


    return render(request,"shopkeeper/seller-manage-products.html",context)

@checkLogin
def delete_product(request, pk):
    uid = request.uid
    product = Product.objects.get(id=pk)

    if product:
        product.delete()
        return redirect("shopkeeper:manage-product")
    else:
        return redirect("shopkeeper:manage-product")
    
@checkLogin
def edit_product(request, pk):
    uid = request.uid
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()

    context = {
        'product' : product,
        'categories' : categories,
        'unit_choice' : Product.UNIT_CHOICES
    }

    return render(request,"shopkeeper/seller-edit-product.html",context)

@checkLogin
def update_product(request):
    uid = request.uid
    
    product_id = request.POST['id']

    product = Product.objects.get(id = product_id)

    product.product_name = request.POST['product_name']
    product.sku = request.POST['sku']
    category = request.POST['category']
    product.Category_fk = Category.objects.get(id = category)
    product.base_price = request.POST['base_price']
    product.discount_price = request.POST['discount_price']
    product.stock_qty = request.POST['stock_qty']
    print(request.POST)
    product.unit = request.POST['unit']
    product.description = request.POST['description']

    if "images" in request.FILES:
        product.images = request.FILES['images']
        
    product.save()

    return redirect("shopkeeper:manage-product")