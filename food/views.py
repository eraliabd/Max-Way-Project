import json
from django.db.models import Count, Max
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Category, Order, OrderProduct, Customer
from .forms import CustomerForm, OrderForm
from .services import get_product_by_id


def get_product_api(request):  # "+" bosilib buyurtmani to'g'ridan to'g'ri bazadan karzinaga olib kelish uchun
    if request.GET:
        product = get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)


def home_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    many_sold = (
        OrderProduct.objects.values('product_id', 'product__title', 'product__image').
            annotate(count=Count('product_id')).order_by('-count')[:1]
    )  # Ko'p sotilgan product

    new_product = (
        Product.objects.values('id', 'title', 'image').
            annotate(count=Max('id')).order_by('-id')[:1]
    )  # Yangi qo'shilgan product

    orders = []
    order_list = request.COOKIES.get('orders')  # Cookie'dan buyurtmalar ro'yxatini oldik
    total_price = request.COOKIES.get('total_price', 0)  # Cookie'dan buyurtmalarning umumiy narxini oldik
    print("orders >>", order_list)
    print("price >>", total_price)

    if order_list:
        for key, value in json.loads(order_list).items():
            print(key, value)
            orders.append(
                {
                    "product": Product.objects.get(pk=int(key)),
                    "count": value
                }
            )
    context = {
        'products': products,
        'categories': categories,
        'total_price': total_price,
        'orders': orders,
        'many_sold': many_sold,
        'new_product': new_product,
    }
    response = render(request, 'food/index.html', context)
    response.set_cookie("cookie", "hello")
    return response


def main_order(request):  # order.html dan bazaga saqlash uchun qurilgan funksiya
    model = Customer()
    if request.POST:
        try:
            model = Customer.objects.get(phone_number=request.POST.get("phone_number", 0))
        except:
            model = Customer()
        form = CustomerForm(request.POST or None, instance=model)
        if form.is_valid():
            customer = form.save()
            formOrder = OrderForm(request.POST or None, instance=Order())
            if formOrder.is_valid():
                order = formOrder.save(customer=customer)
                print("order:", order)
                order_list = request.COOKIES.get("orders")

                for key, value in json.loads(order_list).items():
                    product = get_product_by_id(int(key))

                    counts = value
                    order_product = OrderProduct(
                        count=counts,
                        price=product['price'],
                        product_id=product['id'],
                        order_id=order.id
                    )
                    order_product.save()
                return redirect("food:home_page")
            else:
                print(formOrder.errors)
        else:
            print(form.errors)

    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    order_list = request.COOKIES.get('orders')
    total_price = request.COOKIES.get('total_price')

    if order_list:
        for key, value in json.loads(order_list).items():
            orders.append(
                {
                    "product": Product.objects.get(pk=int(key)),
                    "count": value
                }
            )
    context = {
        'products': products,
        'categories': categories,
        'total_price': total_price,
        'orders': orders,
    }
    response = render(request, 'food/order.html', context)
    response.set_cookie("cookie", "hello")
    return response
