from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('register/signup/', views.SignUpView.as_view(), name="signup"),
    path('home/', views.home, name="home"),
    path('login/', views.login_page, name="login_page"),
    path('logout/', views.logout_page, name="logout_page"),

    path('category/create/', views.category_create, name="category_create"),
    path('category/<int:pk>/edit/', views.category_edit, name="category_edit"),
    path('category/<int:pk>/delete/', views.category_delete, name="category_delete"),
    path('category/list/', views.category_list, name="category_list"),

    path('product/create/', views.product_create, name="product_create"),
    path('product/<int:pk>/edit/', views.product_edit, name="product_edit"),
    path('product/<int:pk>/delete/', views.product_delete, name="product_delete"),
    path('product/list/', views.product_list, name="product_list"),

    path('user/create/', views.user_create, name="user_create"),
    path('user/<int:pk>/edit/', views.user_edit, name="user_edit"),
    path('user/<int:pk>/delete/', views.user_delete, name="user_delete"),
    path('user/list/', views.user_list, name="user_list"),

    path('order/list/', views.order_list, name="order_list"),

    path('profile', views.profile, name="profile_list"),

    path('orderproduct/<int:id>/list/', views.orderproduct_list, name="orderproduct_list"),
    path('customerorder/<int:id>/list/', views.customerorder_list, name="customerorder_list"),
]