from django.db    import models

class Seller(models.Model):
    email            = models.EmailField(max_length=200, unique=True)
    name             = models.CharField(max_length=50, null=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sellers'


class Buyer(models.Model):
    email            = models.EmailField(max_length=200, unique=True)
    name             = models.CharField(max_length=50, null=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'buyers'


class SellerInfo(models.Model):
    seller         = models.ForeignKey(Seller, on_delete=models.CASCADE)
    password       = models.CharField(max_length=400)
    company_name   = models.CharField(max_length=100, null=True)
    company_type   = models.CharField(max_length=100, null=True)
    company_number = models.CharField(max_length=200, null=True)
    address        = models.CharField(max_length=500, null=True)
    phone_number   = models.IntegerField(null=True)
    bank_account   = models.IntegerField(null=True)
    is_deleted     = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seller_info'


class BuyerInfo(models.Model):
    buyer        = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    password     = models.CharField(max_length=400)
    phone_number = models.IntegerField(null=True)
    is_deleted   = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'buyer_info'
