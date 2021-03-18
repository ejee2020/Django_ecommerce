from django.shortcuts import render, get_object_or_404
from django.core import serializers


# Create your views here.
from .models import *
from .forms import *
from cart.forms import AddProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.base import View
from django.http import JsonResponse
from django.db.models.query import EmptyQuerySet
from order.models import *
import json
from django.http import HttpResponse, HttpResponseRedirect
from decimal import Decimal
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


@login_required
def settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'shop/settings.html', {
        'form': form
    })


@login_required
def orders(request):
    user = request.user
    orders = Order.objects.filter(author=user)
    return render(request, 'shop/orders.html', {'orders': orders})


def support_detail(request, support_id):
    support = Support.objects.get(id=support_id)
    return render(request, 'shop/support_detail.html', {'support': support})


def review_detail(request, review_id):
    review = Review.objects.get(id=review_id)
    return render(request, 'shop/review_detail.html', {'review': review})


def create_review(request):
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save()
        return JsonResponse({})


def review_write(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ReviewForm(initial={'author': request.user,
                               'product': product, 'stars': 5})
    return render(request, 'shop/review_write.html', {'form': form})


def completeOrder(request):
    if request.is_ajax():
        id = request.POST.get('order_id')
        order = Order.objects.get(id=id)
        order.paid = True
        order.save()
        return JsonResponse({'url': reverse('shop:product_all')})
    else:
        return JsonResponse({}, status=401)


def redirect(request):
    if request.is_ajax():
        order_transaction = request.POST.get('merchant_id')
        order_transaction = OrderTransaction.objects.get(id=order_transaction)
        order = order_transaction

        return JsonResponse({
            'url': reverse('shop:paypal', args=[order.id])
        })
    else:
        return JsonResponse({}, status=401)


def paypal(request, order):
    order_transaction = request.POST.get('merchant_id')
    order_transaction = OrderTransaction.objects.get(id=order)
    amount = order_transaction.amount
    order = order_transaction.order

    return render(request, 'shop/paypal.html', {'order': order, 'amount': amount})


@login_required
def supportlist(request):
    supportlist = SupportList.objects.get(
        user=request.user)
    supportlist = supportlist.supports.all()
    return render(request, 'shop/supportlist.html', {'supportlist': supportlist})


@login_required
def create_support(request):
    if request.method == 'POST':
        # 입력받은 정보를 후처리
        form = SupportCreateForm(request.POST)
        if form.is_valid():
            support = form.save()
            supportlist = SupportList.objects.get(
                user=request.user)  # wishlist was never made
            supportlist.supports.add(support)
            supportlist = supportlist.supports.all()
            return render(request, 'shop/supportlist.html', {'supportlist': supportlist})
    else:
        form = SupportCreateForm(initial={'author': request.user})
    return render(request, "shop/support.html", {"form": form})


@login_required
def remove_from_wishlist(request, id):
    wishlist = WishList.objects.get(
        user=request.user)
    product = get_object_or_404(Product, id=id)
    wishlist.items.remove(product)
    wishlist = wishlist.items.all()
    return render(request, 'shop/wishlist.html', {'wishlist': wishlist})


@login_required
def wishlist(request):
    wishlist = WishList.objects.get(
        user=request.user)
    wishlist = wishlist.items.all()
    return render(request, 'shop/wishlist.html', {'wishlist': wishlist})


@login_required
def put_into_wishlist(request, id):
    wishlist = WishList.objects.get(
        user=request.user)  # wishlist was never made
    wishlist.items.add(Product.objects.get(id=id))
    product = get_object_or_404(Product, id=id)
    add_to_cart = AddProductForm(initial={'quantity': 1})
    reviews = Review.objects.filter(product__id=id)
    return render(request, 'shop/detail.html', {'product': product, 'add_to_cart': add_to_cart, 'reviews': reviews})


def sort_in_slug(request, sort_slug=None):
    sorts = Sorted.objects.all()
    if request.session['current_category'] == "":
        current_category = None
    else:
        current_category = Category.objects.get(
            id=request.session['current_category'])
    categories = Category.objects.all()
    products = Product.objects.filter(
        pk__in=request.session['display_queryset'])
    if sort_slug:
        current_sort = get_object_or_404(Sorted, slug=sort_slug)
        request.session['current_sort'] = current_sort.id
    slug = current_sort.slug
    if (slug == "alphabetically"):
        products = products.order_by("name")
    elif (slug == "price-high-low"):
        products = products.order_by("-price")
    elif (slug == "price-low-high"):
        products = products.order_by("price")
    elif (slug == "recent"):
        products = products.order_by("-created")
    else:
        products = products.order_by("-view")
    temp = helper(products)
    brands = temp[0]
    sizes = temp[1]
    colors = temp[2]
    prices = temp[3]
    return render(request, 'shop/list.html', {'current_sort': current_sort,
                                              'current_category': current_category,
                                              'sorts': sorts,
                                              'categories': categories,
                                              'products': products, 'brands': brands, 'sizes': sizes,
                                              'colors': colors, 'prices': prices})


@login_required
def product_in_category(request, category_slug=None):
    if 'current_sort' not in request.session:
        request.session['current_sort'] = ""
    current_user = request.user
    wishlist = WishList.objects.filter(
        user=current_user)
    if len(wishlist) == 0:
        new_wishlist = WishList(
            user=current_user)
        new_wishlist.save()

    supportlist = SupportList.objects.filter(
        user=current_user)
    if len(supportlist) == 0:
        new_supportlist = SupportList(
            user=current_user)
        new_supportlist.save()

    current_category = None
    categories = Category.objects.all()
    sorts = Sorted.objects.all()
    products = Product.objects.filter(available_display=True)
    temp = helper(products)
    brands = temp[0]
    sizes = temp[1]
    colors = temp[2]
    prices = temp[3]
    display = [product.id for product in products]
    request.session['display_queryset'] = display
    request.session['current_category'] = ""
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
        display = [product.id for product in products]
        request.session['display_queryset'] = display
        request.session['current_category'] = current_category.id
        all_products = False
    else:
        all_products = True
    return render(request, 'shop/list.html', {'current_category': current_category,
                                              'categories': categories,
                                              'products': products, 'brands': brands, 'sizes': sizes,
                                              'colors': colors, 'prices': prices, 'sorts': sorts, 'all_products': all_products})


def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id)
    add_to_cart = AddProductForm(initial={'quantity': 1})
    reviews = Review.objects.filter(product__id=id)
    return render(request, 'shop/detail.html',
                  {'product': product, 'add_to_cart': add_to_cart, 'reviews': reviews})


def search_bar(request):
    try:
        q = request.GET.get('q')
    except:
        q = None

    queryset = []
    categories = Category.objects.all()
    current_category = None
    sorts = Sorted.objects.all()
    if q:
        template = "shop/search.html"
        split = q.split()
        for word in split:
            products = Product.objects.filter(Q(brand__icontains=word) |
                                              Q(name__icontains=word) |
                                              Q(description__icontains=word)).distinct()
            for product in products:
                queryset.append(product)
        display = [product.id for product in queryset]
        request.session['display_queryset'] = display
        request.session['current_category'] = ""
    else:
        template = "shop/list.html"
        queryset = None
        display = []
        request.session['current_category'] = ""

    return render(request, template, {"queryset": queryset, "categories": categories, "current_category": current_category, "sorts": sorts})


def helper(products):
    brands = []
    sizes = []
    colors = []
    price_max = 0
    prices = []
    for p in products:
        brand = p.brand
        size = p.size
        color = p.color
        price = p.price
        if price > price_max:
            price_max = price
        if brand not in brands:
            brands.append(brand)
        if size not in sizes:
            sizes.append(size)
        if color not in colors:
            colors.append(color)
    price_digit = str(price_max)[0]
    for i in range(int(price_digit) + 1):
        start = i * 100
        end = (i + 1) * 100
        prices.append("$" + str(start) + " ~ " + "$" + str(end))
    return [brands, sizes, colors, prices]


class FilterAjaxView(View):
    def post(self, request, *args, **kwargs):
        products = Product.objects.filter(
            pk__in=request.session['display_queryset'])
        color = request.POST['color']
        if color != "Color":
            products = products.filter(color=color)

        size = request.POST['size']
        if size != "Size":
            products = products.filter(size=size)

        brand = request.POST['brand']
        if brand != "Brand":
            products = products.filter(brand=brand)

        price = request.POST['price']
        if price != "Price Range":
            split = price.split()
            minimum = split[0][1:]
            maximum = split[2][1:]
            products = products.filter(price__lt=Decimal(maximum))
            products = products.filter(price__gt=Decimal(minimum))

        display = [product.id for product in products]
        print(display)
        request.session['display_queryset'] = display
        data = {'url': reverse('shop:filter2')}
        return JsonResponse(data)


def filter(request):
    sorts = Sorted.objects.all()
    if request.session['current_category'] == "":
        current_category = None
    else:
        current_category = Category.objects.get(
            id=request.session['current_category'])
    categories = Category.objects.all()
    products = Product.objects.filter(
        pk__in=request.session['display_queryset'])
    if request.session['current_sort'] == "":
        current_sort = None
    else:
        current_sort = Sorted.objects.filter(
            id=request.session['current_sort'])
    temp = helper(products)
    brands = temp[0]
    sizes = temp[1]
    colors = temp[2]
    prices = temp[3]
    all_products = False
    print('here')
    return render(request, 'shop/list.html', {
        'current_category': current_category,
        'sorts': sorts,
        'categories': categories,
        'products': products, 'brands': brands, 'sizes': sizes,
        'colors': colors, 'prices': prices, 'all_products': all_products})
