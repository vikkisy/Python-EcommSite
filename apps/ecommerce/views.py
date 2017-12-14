# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.db.models import Count
from django.db.models import Sum
from django.shortcuts import render, redirect, HttpResponse
import operator
from models import *
from .forms import AddProduct

# Create your views here.


def index(request):
    items= Item.objects.all()
    context = {
        'category': Item.objects.values('category').distinct().annotate(count=Count('category')),
        'items': items,
    }
    return render(request, 'ecommerce/home.html', context)

def search(request):
    items=Item.objects.filter(name__startswith=request.POST['search'])
    return render(request, 'ecommerce/all_items.html', {"items": items})


def adminsearch(request):
    items=Item.objects.filter(name__startswith=request.POST['adminsearch'])
    return render(request, 'ecommerce/products_search.html', {"items": items})

def searchcat(request):
    items=Item.objects.filter(category=request.POST['category'])
    return render(request, 'ecommerce/all_items.html', {'items': items, 'category': request.POST['category']})

def sortby(request):
    if request.POST['sorted'] == 'popularity':
        items=Item.objects.all().order_by(request.POST['sorted']).reverse()
    else:
        items=Item.objects.all().order_by(request.POST['sorted'])
    category = request.POST['sorted']
    context={
        'items': items,
        'category': category
    }
    return render(request, 'ecommerce/all_items.html', context)

def products_search(request):
    items=Items.objects.all()
    context = {"items":items}
    return render(request, 'ecommerce/products_search.html', context)

def all_items(request):
    items= Item.objects.all()
    context = {
        'category': Item.objects.values('category').distinct().annotate(count=Count('category')),
        'items': items,
    }
    return render(request, 'ecommerce/all_items.html', context)

def item(request, item_id):
    c = Item.objects.get(id=item_id)
    cat_get = c.category
    context = {
        'all_items': Item.objects.filter(category=cat_get), # need to pass in category......
        'item': Item.objects.get(id=item_id)
    }
    return render(request, 'ecommerce/item.html', context)

def addcart(request):
    qty = request.POST['quantity_added']
    if not 'cart' in request.session:
        new_cart = Cart.objects.create()
        new_cartitem = CartItem.objects.create(
        quantity=qty,
        item = Item.objects.get(id=request.POST['item_id']),
        cart = new_cart)
        request.session['cart'] = new_cart.id
    else:
        CartItem.objects.create(
        cart = Cart.objects.get(id=request.session['cart']) ,
        quantity= qty,
        item = Item.objects.get(id=request.POST['item_id']))
    return redirect('/')

def admin(request):
    return render(request, 'ecommerce/index.html')


def login(request):
    if request.method == "POST":
        errors = Adminuser.objects.basic_login_validator(request.POST)
        # if len(errors):
        #     for tag, error in errors.iteritems():
        #         messages.error(request,error, extra_tags=tag)
        #         return redirect('/')
        # else:
        #     user = Adminuser.objects.get(email = request.POST['email'])
        #     if not 'admin' in request.session:
        #         request.session['admin'] = adminuser.id
    return redirect('/orders')

def orders(request):
    context = {
        "order_details": Order.objects.all()
    }
    return render(request, 'ecommerce/orders.html', context)

def edit(request):
    return redirect('/products')

def delete(request):
    if request.method == "POST":
        i = Item.objects.get(id = request.POST['id'])
        i.delete()
    return redirect('/products')

def products(request):
    items = Item.objects.all()
    return render(request, 'ecommerce/products.html', {'items': items})

def add(request):
    return redirect('/products')

def logout(request):

    return redirect('/admin')


def cart(request):
    a = Cart.objects.filter(pk=request.session['cart']).values('cart_items__item__id').annotate(Count('cart_items__quantity'))
    b = CartItem.objects.filter(cart=request.session['cart']).aggregate(Sum('quantity'))
    print b
    # a = CartItem.objects.annotate(Count('quantity')).values("item").filter(cart=request.session['cart'])
    item_info = list(a)
    print list(a)
    print list(b)
    item_list = []
    c = operator.itemgetter('cart_items__item__id')
    for cart_items__quantity in item_info:
        item_list.append(c(cart_items__quantity))
    print item_list

    # for item in item_info:
    #     print [(items['item.cart_items__item__id'],items['item.cart_items__quantity']) for items in item_info]

        # item['item']= Item.objects.filter(id=item.cart_items__item__id)
        # item_info.append(item)
    # print item_info
    # for item_info in b
    # print item_info
    context = {
        "cart": list(a),
        "item": Item.objects.filter(id__in=item_list),
    }

    # print context
    return render(request, 'ecommerce/cart.html', context)

def process_order(request):

    ship = Shipping.objects.create(
    first_name=request.POST['first_name'],
    last_name=request.POST['last_name'],
    address=request.POST['address'],
    address2=request.POST['address2'],
    city=request.POST['city'],
    state=request.POST['state'],
    zipcode=request.POST['zipcode']
    )

    bill = Billing.objects.create(
    first_name=request.POST['bfirst_name'],
    last_name=request.POST['blast_name'],
    address=request.POST['baddress'],
    address2=request.POST['baddress2'],
    city=request.POST['bcity'],
    state=request.POST['bstate'],
    zipcode=request.POST['bzipcode']
    )

    Order.objects.create(
    billing = bill,
    shipping = ship,
    cart = Cart.objects.get(id=request.session['cart'])
    )

    return redirect('/confirmation')

def confirmation(request):
    del request.session['cart']
    return render(request, 'ecommerce/confirmation.html')

def addproduct(request):
    if request.method == "POST":
        form = AddProduct(request.POST)
        if form.is_valid():
            return redirect('/')
    else:
        form= AddProduct()
    return render(request, 'ecommerce/addproduct.html', {'form':form})

def show_order(request, order_id):
    o = Order.objects.get(id=order_id)
    cart_id = o.cart.id
    print cart_id
    a = Cart.objects.filter(pk=cart_id).values('cart_items__item__id').annotate(Count('cart_items__quantity'))
    item_info = list(a)
    item_list = []
    c = operator.itemgetter('cart_items__item__id')
    for cart_items__quantity in item_info:
        item_list.append(c(cart_items__quantity))

    context = {
        "cart": list(a),
        "item": Item.objects.filter(id__in=item_list),
        "order_details": Order.objects.get(id=order_id)
    }
    return render(request, 'ecommerce/specific_order.html', context)
# Create shopping page
# View all items page with categories and search
# Specific Item Page to buy
# Checkout page with shipping and billing form/ with price and items in shopping cart
# --ADMIN
# -Orders
# Search thru Orders
# View All Orders with seperate pages for items
# Specifc order page with items and status
# --Products
# View all products and add new products
# Edit product popup
  # {% for item in items %}
  # <img src="static/ecommerce/img/{{item.image}}" alt="">
  # {% endfor %}
