from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import pytz
import requests
from django.db.models import Sum, F
from django.shortcuts import render
from .models import Product, CartItem
import matplotlib.pyplot as plt
import io
import base64

from base.forms import CustomUserCreationForm, OrderForm, ProductForm, ReviewForm
from .models import FAQ, Cart, Contact, Coupon, Job, New, Order, Product, Profile, Review, CartItem

def home(request, category=None):
    popular_categories = Product.objects.values('category').annotate(total_quantity=Sum('cartitem__quantity')).order_by('-total_quantity')

    profitable_categories = Product.objects.values('category').annotate(total_revenue=Sum(F('cartitem__quantity') * F('price'))).order_by('-total_revenue')

    most_popular_category = popular_categories.first()
    most_profitable_category = profitable_categories.first()
    current_time = timezone.now()
    user_tz = pytz.timezone('Europe/Moscow')
    user_time = current_time.astimezone(user_tz)
    latest_new = New.objects.latest('id')
    try:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            user_role = profile.role
        else:
            user_role = 'none'
    except Profile.DoesNotExist:
        user_role = 'none'

    api_url = "https://catfact.ninja/fact"
    response = requests.get(api_url)

    if response.status_code == 200:
        cat_fact = response.json()['fact']

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'products': products,
        'user_role': user_role,
        'cat_fact':cat_fact,
        'latest_new':latest_new,
        'user_timezone': user_tz,
        'current_time': user_time,
        "most_popular_category": most_popular_category,
        "most_profitable_category": most_profitable_category
    }

    return render(request, "base/home.html", context)


def about_us(request):
    return render(request, 'base/about.html')

def news(request):
    news_list = New.objects.all()
    return render(request, "base/news.html", {'news_list': news_list})

def contact(request):
    contacts = Contact.objects.all()
    return render(request, "base/contact.html", {'contacts': contacts})

def faq(request):
    faq_list = FAQ.objects.all()
    return render(request, "base/faq.html", {'faq_list':faq_list})

def conf(request):
    api_url="https://favqs.com/api/qotd"

    response = requests.get(api_url)

    if response.status_code == 200:
        quote_data = response.json()['quote']
        quote_text = quote_data['body']

    return render(request, "base/conf.html", {'quote_text':quote_text})

def vacancies(request):
    jobs = Job.objects.all()
    return render(request, "base/vacancies.html", {'jobs': jobs})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, "base/review_list.html", {'reviews': reviews})

@login_required(login_url='login')
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('base/review_list.html')
    else:
        form = ReviewForm()
    return render(request, "base/review.html", {'form': form})

def coupons(request):
    active_coupons = Coupon.objects.filter(active=True)
    inactive_coupons = Coupon.objects.filter(active=False)
    return render(request, "base/coupons.html", {'active_coupons': active_coupons, 'inactive_coupons': inactive_coupons})

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")

    context ={'page':page}
    return render(request, "base/login_register.html", context)
    
def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.birth_date = form.cleaned_data.get('birth_date')
            user.phone_number = form.cleaned_data.get('phone_number')
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred!")

    return render(request, 'base/login_register.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, is_new=True)
    cart_product, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    return redirect('home')

@login_required(login_url='login')
def view_cart(request):
    cart = Cart.objects.get(user=request.user, is_new=True)
    cartproduct_set = CartItem.objects.filter(cart=cart)
    return render(request, 'base/cart.html', {'cartproduct_set': cartproduct_set})

@login_required(login_url='login')
def create_order(request):
    cart = Cart.objects.get(user=request.user, is_new=True)
    cart_items = CartItem.objects.filter(cart=cart)
    
    coupon_number = request.GET.get('coupon_number')
    coupon = Coupon.objects.get(number=coupon_number)
    title_value = coupon.title
    numeric_value = int(title_value)

    total_payment = sum(item.product.price * item.quantity for item in cart_items)

    total_payment -= numeric_value

    if request.method == 'POST':
        form = OrderForm(request.POST)
        coupon_number = request.POST.get('coupon_number')
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart_items:
                order.items.add(item)

            order.total_amount = total_payment
            order.save()
            cart.is_new = False
            cart.save()
            new_cart = Cart.objects.create(user=request.user, is_new=True)
            return redirect('home')  # Redirect to home page after successful order placement
    else:
        
        form = OrderForm()

    context = {
        'cart_items': cart_items,
        'form': form,
        'total_payment': total_payment,
    }
    return render(request, 'base/create_order.html', context)

@login_required(login_url='login')
def order_list(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role == 'staff' or profile.role=='admin':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    context = {
        'orders': orders,
        'user_role': profile.role 
    }
    return render(request, 'base/order_list.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')  # ��� ����-���� ���
    else:
        form = ProductForm(instance=product)
    return render(request, 'base/edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('home')  # Обновите это с именем вашего представления списка продуктов
    return render(request, 'base/delete_product.html', {'product': product})

def get_category_data():
    # Наиболее популярные категории товаров
    category_data = Product.objects.values('category').annotate(
        total_quantity=Sum('cartitem__quantity'),
        total_revenue=Sum(F('cartitem__quantity') * F('price'))
    ).order_by('-total_quantity')

    return category_data

def prepare_chart_data(category_data):
    categories = [item['category'] for item in category_data]
    quantities = [item['total_quantity'] for item in category_data]
    revenues = [item['total_revenue'] for item in category_data]

    return categories, quantities, revenues

def plot_category_data(categories, quantities, revenues):
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Total Quantity', color=color)
    ax1.bar(categories, quantities, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Total Revenue', color=color)
    ax2.plot(categories, revenues, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return image_base64

def category_chart_view(request):
    category_data = get_category_data()
    categories, quantities, revenues = prepare_chart_data(category_data)
    chart_image = plot_category_data(categories, quantities, revenues)

    context = {
        'chart_image': chart_image,
    }

    return render(request, 'base/category_chart.html', context)