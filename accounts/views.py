from django.shortcuts import render , redirect
from .models import *
from django.views.generic import ListView
from .forms import OrderForm, CustomerForm, CreateUser
from django.contrib.auth import login,authenticate,logout
from . filters import OrderFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users, admin_only
from django.contrib.auth.models import Group


@login_required(login_url='login')
@admin_only
def homePage(request):
    customer = Customer.objects.all()
    order = Order.objects.all()
    
    total_customer = customer.count()
    total_order = order.count()
    total_delivered = order.filter(status="Delivered").count()
    total_pending = order.filter(status="Pending").count()

    context = {
    "customers":customer,
    "orders":order,
    "total_customer":total_customer,
    "total_order":total_order,
    "total_delivered":total_delivered,
    "total_pending":total_pending
    } 
    return render(request,'dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def productview(request):

    products = Product.objects.all()
    return render(request, 'product.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def customer(request,pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    total_order = orders.count()
    orderfilter = OrderFilter(request.GET,queryset=orders)
    orders = orderfilter.qs
    context = {"customers":customers,
                "orders":orders,
                "total_orders":total_order,
                "orderfilter":orderfilter,
    }
    
    return render(request,'customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    context = {"form":form}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'create_order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form":form}
    return render(request,'create_order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    context = {"order":order}
    if request.method == "POST":
        order.delete()
        return redirect('/')
    return render(request,'delete_order.html',context)

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def createCustomer(request):
    form = CustomerForm
    context = {"form":form}
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'create_customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def updateCustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form":form}
    return render(request,'update_customer.html',context)

def signUp(request):
    form = CreateUser
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()

            #assigning  user to a specific group and creating a customer profile for a user during user creation
            # Now handled by by signals 
            '''group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user = user,
                name = user.username
            )'''

            username = form.cleaned_data.get('username')
            messages.success(request,"account created succesfully for "+ str(username))
            return redirect('login')
    context = {"form":form}
    return render(request,'reg.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user1 = authenticate(request,username=username,password=password)
        if user1 is not None:
            login(request,user1)
            return redirect('home')
        else:
            messages.info(request,"invalid username or password")

    return render(request,'login.html')

def logoutPage(request):
    logout(request)
    return redirect('login') 

@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    total_delivered = orders.filter(status="Delivered").count()
    total_pending = orders.filter(status="Pending").count()

    context = {'orders':orders,'total_order':total_order,'total_delivered':total_delivered,'total_pending':total_pending}
    return render(request,'user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
         form = CustomerForm(request.POST,request.FILES, instance=customer)
         if form.is_valid():
             form.save()
             messages.success(request,"Profile Updated Successfully!")
    context = {'form':form}
    return render(request,'account_settings.html',context)
