from account.models import Buyer, Seller
from product.models import Product, ProductOption

from django.db import models

class Cart(models.Model):
    buyer           = models.ForeignKey(Buyer, on_delete = models.CASCADE)
    product         = models.ForeignKey(Product, on_delete = models.CASCADE)
    product_option  = models.ForeignKey(ProductOption, on_delete = models.CASCADE, null=True)
    product_name    = models.CharField(max_length = 100)
    quantity        = models.IntegerField()
    is_deleted      = models.BooleanField(default=False)
    is_buy          = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'carts'

class Order(models.Model):
    buyer              = models.ForeignKey(Buyer, on_delete = models.CASCADE)
    receiver_name      = models.CharField(max_length = 100)
    order_amount       = models.IntegerField(null=True)
    total_amount       = models.IntegerField(null=True)
    total_price        = models.DecimalField(max_digits = 10, decimal_places = 2, null=True)
    created_at         = models.DateTimeField(auto_now_add = True)
    updated_at         = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'orders'

class OrderProduct(models.Model):
    seller           = models.ForeignKey(Seller, on_delete = models.CASCADE)
    order            = models.ForeignKey(Order, on_delete = models.CASCADE)
    product          = models.ForeignKey(Product, on_delete = models.CASCADE)
    order_status     = models.ForeignKey('OrderStatus', on_delete = models.CASCADE)
    product_name     = models.CharField(max_length = 100)
    origin_price     = models.DecimalField(max_digits = 10, decimal_places = 2)
    price            = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity         = models.IntegerField()
    departure_time   = models.DateField(null=True)
    arrival_time     = models.DateField(null=True)
    created_at       = models.DateTimeField(auto_now_add = True)
    updated_at       = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'order_products'

class OrderProductOption(models.Model):
    order_product  = models.ForeignKey(OrderProduct, on_delete = models.CASCADE)
    product_option = models.ForeignKey(ProductOption, on_delete = models.CASCADE, null=True)
    option1_name   = models.CharField(max_length = 100, null=True, default=None)
    option1_value  = models.CharField(max_length = 100, null=True, default=None)
    option2_name   = models.CharField(max_length = 100, null=True, default=None)
    option2_value  = models.CharField(max_length = 100, null=True, default=None)
    option3_name   = models.CharField(max_length = 100, null=True, default=None)
    option3_value  = models.CharField(max_length = 100, null=True, default=None)
    add_price      = models.DecimalField(max_digits = 10, decimal_places = 2)
    created_at     = models.DateTimeField(auto_now_add = True)
    updated_at     = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'order_product_options'

class OrderStatus(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'order_status'

