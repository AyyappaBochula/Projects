from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from .models import Product, Category, Customer, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest


def home(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count() 
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'cart_item_count': cart_item_count,
        'products': products,  
        'categories': categories, 
    }
    return render(request, 'home.html', context)
def about(request):
    return render(request, 'about.html',)

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'view_product.html', {'product': product})
def cart_view(request):
    cart_items = []
    total_amount = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            for cart_item in cart.items.all():
                total_price = cart_item.total_price()  # Call the CartItem method
                total_amount += total_price
                cart_items.append({
                    'product': cart_item.product,
                    'size': cart_item.size,
                    'quantity': cart_item.quantity,
                    'price': cart_item.product.sale_price if cart_item.product.is_on_sale else cart_item.product.price,  # Use effective price
                    'total_price': total_price,
                })
    else:
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            price = product.sale_price if product.is_on_sale else product.price
            total_price = price * quantity
            total_amount += total_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total_price': total_price
            })

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

def add_to_cart(request, product_id):
    if request.method == "POST" and request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        size = request.POST.get('size')  # Get the selected size
        quantity = request.POST.get('quantity', 1)  # Default to 1 if no quantity is provided

        # Ensure quantity is an integer
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1  # Fallback to 1 if the quantity is invalid

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity  # Increment quantity if item already in cart
        cart_item.save()

        return redirect('home')
    return redirect('home')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]  
        request.session['cart'] = cart
    return redirect('cart')


def update_cart_item(request, product_id):
    if request.method == "POST" and request.user.is_authenticated:
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1  # Default to 1 if invalid

        if quantity < 1:
            quantity = 1  # Prevent negative or zero quantity

        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if cart_item:
                cart_item.quantity = quantity
                cart_item.save()

        return redirect('cart')
    return redirect('cart')

def cart_view(request):
    cart_items = []
    total_amount = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            for cart_item in cart.items.all():
                total_price = cart_item.total_price()
                total_amount += total_price
                cart_items.append({
                    'product': cart_item.product,
                    'size': cart_item.size,
                    'quantity': cart_item.quantity,  # Ensure quantity is passed here
                    'total_price': total_price
                })
        else:
            # If the cart does not exist
            cart_items = []
    else:
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total_price = product.price * quantity
            total_amount += total_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price
            })

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_item = cart.items.filter(product_id=product_id).first()
            if cart_item:
                cart_item.delete()
    else:
        cart = request.session.get('cart', {})
        product_id_str = str(product_id) 
        if product_id_str in cart:
            del cart[product_id_str]
            request.session['cart'] = cart

    return redirect('cart')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.create_user(username=email, email=email, password=password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=password1  
            )
            customer.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
    return render(request, 'signup.html')


def custom_logout_view(request):
    logout(request)
    return redirect('home')  


def category_summary(request):
    products = Product.objects.all()
    return render(request, 'category_summary.html', {'products': products})

def category_view(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})


@login_required
def buy_now(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        order_details = []
        total_amount = 0
        if cart:
            for cart_item in cart.items.all():
                total_price = cart_item.total_price()
                total_amount += total_price
                order_details.append({
                    'name': cart_item.product.name,
                    'price': cart_item.product.price,
                    'quantity': cart_item.quantity,
                    'total_price': total_price
                })
            
            cart.items.all().delete()
        
        return render(request, 'buy_now.html', {
            'order_details': order_details,
            'total_amount': total_amount
        })
    return redirect('cart')


