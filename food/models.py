from django.db import models

######### MODELlar ########
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=False, null=False)
    image = models.ImageField(upload_to='product_image/')
    price = models.DecimalField(max_digits=50, decimal_places=2, blank=False, null=False)
    cost = models.DecimalField(max_digits=50, decimal_places=2, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Customer(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.BigIntegerField(blank=False, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    payment = models.IntegerField(blank=False, null=False)
    status = models.IntegerField(blank=True, null=False, default=1)
    address = models.CharField(max_length=250, blank=False, null=False)
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address}"

class OrderProduct(models.Model):
    count = models.IntegerField(blank=False, null=False)
    price = models.DecimalField(max_digits=50, decimal_places=2, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.count} {self.product}"
