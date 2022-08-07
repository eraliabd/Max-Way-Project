from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Count

from .forms import CategoryForm, ProductForm, UserForm
from food.models import Category, Customer, Product, OrderProduct, Order
from .services import get_categories, get_products, get_product_by_order, get_order_by_user


######## Admin dashboardga kirishda login bo'lganmi yo'qmi deb tekshirish uchun decorator tayyorlab olganmiz
######## login_required decorator'i orqali ########
def login_required_decorator(func):
    return login_required(func, login_url="dashboard:login_page")


######### DASHBOARD home qismi ##########
@login_required_decorator
def home(request):
    categories = get_categories()
    products = get_products()
    users = Customer.objects.all()
    orders = Order.objects.all()
    top_products = (
        OrderProduct.objects.values('product_id', 'product__title').
            annotate(count=Count('product_id')).order_by('-count')[:10]
    )  # Eng ko'p mijozlar tomonidan tanlangan mahsulotlar top 10 taligini olib keladigan Django ORM qismi
    # print(top_products)

    ctx = {
        "counts": {
            'categories': len(categories),
            'products': len(products),
            'users': len(users),
            'orders': len(orders),
            'top_products': top_products,
        }
    }
    response = render(request, 'dashboard/index.html', ctx)
    response.set_cookie('categories', categories)  ## COOKIES ##
    return response


######### Logout ########
@login_required_decorator
def logout_page(request):
    logout(request)
    response = redirect("dashboard:login_page")
    response.delete_cookie('username')
    response.delete_cookie('password')  ## COOKIES ##
    return response


####### Login ########
def login_page(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)

        if user is not None:
            login(request, user)
            response = redirect("dashboard:home")
            response.set_cookie('username', username)  ## COOKIES ##
            response.set_cookie('password', True)
            return response

    return render(request, "dashboard/login.html")


###### Sign Up #######
class SignUpView(CreateView):  ## CreateView ##
    form_class = UserCreationForm
    success_url = reverse_lazy("dashboard:login_page")
    template_name = "dashboard/signup.html"


######## CATEGORY ########
@login_required_decorator
def category_create(request):
    model = Category()
    form = CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('session', [])
        actions += [f"You created Category: {request.POST.get('name')}"]
        request.session['actions'] = actions

        count = request.session.get('count', 0)
        count += 1
        request.session['count'] = count

        return redirect('dashboard:category_list')
    ctx = {
        'form': form,
    }
    return render(request, 'dashboard/category/form.html', ctx)


@login_required_decorator
def category_edit(request, pk):
    model = Category.objects.get(pk=pk)
    form = CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('session', [])
        actions += [f"You edited Category: {request.POST.get('name')}"]
        request.session['actions'] = actions

        return redirect('dashboard:category_list')
    ctx = {
        'form': form,
        'model': model
    }
    return render(request, 'dashboard/category/form.html', ctx)


@login_required_decorator
def category_delete(request, pk):
    model = Category.objects.get(pk=pk)
    model.delete()

    actions = request.session.get('actions', [])
    actions += [f"You deleted Category: {model}"]
    request.session['actions'] = actions

    count = request.session.get('count', 0)
    if count > 0:
        count -= 1
        request.session['count'] = count
    else:
        count = 0
        request.session['count'] = count

    return redirect("dashboard:category_list")


@login_required_decorator
def category_list(request):
    categories = get_categories()
    ctx = {
        "categories": categories,
    }
    return render(request, "dashboard/category/list.html", ctx)


######### PRODUCT #########
@login_required_decorator
def product_create(request):
    model = Product()
    form = ProductForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('actions', [])
        actions += [f"You created Product: {request.POST.get('title')}"]
        request.session['actions'] = actions

        count = request.session.get('count', 0)
        count += 1
        request.session['count'] = count

        return redirect('dashboard:product_list')
    ctx = {
        'form': form,
    }
    return render(request, 'dashboard/product/form.html', ctx)


@login_required_decorator
def product_edit(request, pk):
    model = Product.objects.get(pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('actions', [])
        actions += [f"You edited Product: {request.POST.get('title')}"]
        request.session['actions'] = actions

        return redirect('dashboard:product_list')
    ctx = {
        'form': form,
        'model': model,
    }
    return render(request, 'dashboard/product/form.html', ctx)


@login_required_decorator
def product_delete(request, pk):
    model = Product.objects.get(pk=pk)
    model.delete()

    actions = request.session.get('actions', [])
    actions += [f"You deleted Category: {model}"]
    request.session['actions'] = actions

    count = request.session.get('count', 0)
    if count > 0:
        count -= 1
        request.session['count'] = count
    else:
        count = 0
        request.session['count'] = count

    return redirect("dashboard:product_list")


@login_required_decorator
def product_list(request):
    products = get_products()
    ctx = {
        "products": products,
    }
    return render(request, "dashboard/product/list.html", ctx)


####### USER ##########
@login_required_decorator
def user_create(request):
    model = Customer()
    form = UserForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()
        return redirect('dashboard:user_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/user/form.html', ctx)


@login_required_decorator
def user_edit(request, pk):
    model = Customer.objects.get(pk=pk)
    form = UserForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()
        return redirect('dashboard:user_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/user/form.html', ctx)


@login_required_decorator
def user_delete(request, pk):
    model = Customer.objects.get(pk=pk)
    model.delete()
    return redirect("dashboard:user_list")


@login_required_decorator
def user_list(request):  ## users ni yig'ib boradi
    users = Customer.objects.all()
    ctx = {
        'users': users
    }
    return render(request, 'dashboard/user/list.html', ctx)


@login_required_decorator
def order_list(request):  ## Buyurtma qayerdan kelganligi
    orders = Order.objects.all()
    return render(request, 'dashboard/order/list.html', {'orders': orders})


@login_required_decorator
def profile(request):  ## Profile ya'ni product yoki category qo'shsam, tahrirlasam va o'chirib yuborsam
    ##  shu hodisalarni ko'rsatib turadi
    return render(request, 'dashboard/profile.html')


@login_required_decorator
def orderproduct_list(request, id):  ## Buyurtmalarni olib keladi
    orderproducts = get_product_by_order(id=id)
    ctx = {
        'orderproducts': orderproducts
    }
    return render(request, "dashboard/productorder/list.html", ctx)


@login_required_decorator
def customerorder_list(request, id):  ## Usha buyurtma bergan mijoz haqida to'liq ma'lumotni olib keladi
    customerorder_list = get_order_by_user(id=id)
    ctx = {
        'customerorder_list': customerorder_list,
    }
    return render(request, 'dashboard/customer_order/list.html', ctx)
