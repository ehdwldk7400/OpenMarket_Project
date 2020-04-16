from django.db       import models
from account.models  import Seller
from mptt.models     import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name       = models.CharField(max_length=50, unique=True)
    parent     = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'categories'

class Product(models.Model):
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller        = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name          = models.CharField(max_length=200)
    origin_price  = models.DecimalField(max_digits = 10, decimal_places = 2)
    stock         = models.IntegerField()
    thumbnail_img = models.TextField(max_length=2000)
    description   = models.TextField(null=True)
    delivery_fee  = models.DecimalField(max_digits = 10, decimal_places = 2)
    is_option     = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    is_discount   = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

class ProductOption(models.Model):
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)
    option1_name  = models.CharField(max_length = 100, null=True, default=None)
    option1_value = models.CharField(max_length = 100, null=True, default=None)
    option2_name  = models.CharField(max_length = 100, null=True, default=None)
    option2_value = models.CharField(max_length = 100, null=True, default=None)
    option3_name  = models.CharField(max_length = 100, null=True, default=None)
    option3_value = models.CharField(max_length = 100, null=True, default=None)
    add_price     = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity      = models.IntegerField()
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_options'

class Cycle(models.Model):
    hour = models.IntegerField()

    class Meta:
        db_table = 'cycles'

class PriceOption(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    cycle       = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    start_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    last_price  = models.DecimalField(max_digits = 10, decimal_places = 2)
    start_at    = models.DateTimeField()
    end_at      = models.DateTimeField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'price_options'

class PriceData(models.Model):
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_option   = models.ForeignKey(PriceOption, on_delete=models.CASCADE)
    cycle          = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    discount_rate  = models.FloatField()
    discount_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    start_date     = models.DateTimeField()
    end_date       = models.DateTimeField()
    is_deleted     = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'price_data'

class ProductImage(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url  = models.TextField(max_length = 2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_images'
