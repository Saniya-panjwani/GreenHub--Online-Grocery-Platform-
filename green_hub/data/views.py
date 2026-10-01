from django.shortcuts import render,redirect
from .models import*
from django.contrib.auth.hashers import make_password,check_password
from .utils import MyCustomSendmail
import random

def checkLogin(view_function):
    def wrapper(request,*args,**kwargs):
        if "email" in request.session:
            try:
                uid = User.objects.get(email = request.session['email'])
                request.uid = uid
                return view_function(request,*args,**kwargs)
            except User.DoesNotExist:
                del request.session["email"]
                return redirect("data:login")
        else:
            return redirect("data:login")
    return wrapper

# Create your views here.
def login(request):
    if "email" in request.session:
        try:
            uid = User.objects.get(email = request.session['email'])
            if uid.role == "shopkeeper":
                return redirect("shopkeeper:dashboard")
            else:
                return redirect("customer:home")
                
        except User.DoesNotExist:
            del request.session["email"]
    else:
        if request.POST:
            email = request.POST['email']
            password = request.POST['password']

            try:
                uid = User.objects.get(email = email)

                if not check_password(password,uid.password):
                    context ={
                        'e_msg' : "invalid password"
                    }
                    return render(request,"data/login.html",context)
                else:
                    if uid.role == "shopkeeper":
                        request.session['email'] = email
                        return redirect("shopkeeper:dashboard")
                    else:
                        request.session['email'] = email
                        return redirect("customer:home") 
            except Exception as e:
                context ={
                    'e_msg' : e
                }
                return render(request,"data/login.html",context)
    return render(request,"data/login.html")

def register(request):
    if request.POST:
        print("----->> button clicked")
        role = request.POST['role']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            context = {
                'e_msg' : "password doesn't match"
            }
            return render(request,"data/registration.html",context)
        
        if User.objects.filter(email = email).exists():
            context = {
                'e_msg' : "email already exists"
            }
            return render(request,"data/registration.html",context)


        try:
            uid = User.objects.create(email = email,
                                    password = make_password(password),
                                    role = role)
            if role == "shopkeeper":
                Shopkeeper.objects.create(
                    user_fk = uid,
                    first_name = first_name,
                    last_name = last_name
                )
                return redirect("data:login")
            else:
                Customer.objects.create(
                    user_fk = uid,
                    first_name = first_name,
                    last_name = last_name
                )
                return redirect("data:login")

        except Exception as e:
            print(e)
            context = {
                'e_msg' : e
            }
            return render(request,"data/registration.html",context)
         
        return render(request,"data/registration.html")
        
    else:
        print("---> only refreshed")
    return render(request,"data/registration.html")

@checkLogin
def logout(request):
    if "email" in request.session:
        del request.session['email']
        return redirect("data:login")


def forgot_password(request):
    if request.POST:
        email = request.POST['email']
        uid = User.objects.get(email = email)
        if uid:
            otp = random.randint(1111,9999)
            uid.otp = otp
            uid.save()

            # request.session["reset_email"] = email
            MyCustomSendmail("Forgot password","mail_template",email,{'otp': otp})
        return render(request,"data/otp.html",{'email' : email})
    else:
        return render(request,"data/forgot_password.html")

def otp_view(request):
    if request.POST:
        email = request.POST['email']
        otp = request.POST['otp']
        uid = User.objects.get(email = email)
        if uid:
            if str(uid.otp) == str(otp):
                return render(request,"data/reset_password.html",{'email' :email})
            else:
                return redirect("data:forgot-password")
        else:
            return render(request,"data/otp.html")
    
def reset_password(request):
    if request.POST:
        email = request.POST['email']
        newpassword = request.POST['newpassword']
        repassword = request.POST['repassword']

        uid = User.objects.get(email = email)

        if newpassword == repassword:
            uid.password = make_password(newpassword)
            uid.save()
            return redirect("data:login")
        else:
            return render(request,"data/reset_password.html",{"email":email,"e_msg":"password do not match"})
    return redirect("data:forgot-password")