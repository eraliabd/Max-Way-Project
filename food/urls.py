from django.urls import path
from .views import home_page, get_product_api, main_order

app_name = "food"

urlpatterns = [
    path('', home_page, name="home_page"),
    path('product/', get_product_api, name="get_product_api"),
    path('order/', main_order, name="main_order"),
]