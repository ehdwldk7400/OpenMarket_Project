import json
import jwt

from my_settings import SECRET_KEY
from .models import(
    Category,
    Product,
    ProductOption,
    Cycle,
    PriceOption,
    PriceData
)
from account.models import Seller, SellerInfo

from django.test import TestCase, Client


class ProductDetailTest(TestCase):

    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = 'food'
        )

        Seller.objects.create(
            id    = 1,
            email = 'a@a.com',
            name  = 'seller'
        )

        SellerInfo.objects.create(
            id           = 1,
            seller_id    = 1,
            password     = 1234,
            company_name = 'Gangwon-Do'
        )

        Product.objects.create(
            id            = 1,
            category_id   = 1,
            seller_id     = 1,
            name          = 'Gangwon-Do Potato',
            origin_price  = 10000,
            stock         = 100,
            thumbnail_img = 'url',
            description   = 'desc',
            delivery_fee  = 2500,
            is_option     = True
        )

        ProductOption.objects.create(
            id            = 1,
            product_id    = 1,
            option1_name  = 'color',
            option1_value = 'black',
            option2_name  = 'size',
            option2_value = 'M',
            add_price     = 2100,
            quantity      = 10,
        )

        ProductOption.objects.create(
            id            = 2,
            product_id    = 1,
            option1_name  = 'color',
            option1_value = 'black',
            option2_name  = 'size',
            option2_value = 'L',
            add_price     = 2200,
            quantity      = 10,
        )

        ProductOption.objects.create(
            id            = 3,
            product_id    = 1,
            option1_name  = 'color',
            option1_value = 'red',
            option2_name  = 'size',
            option2_value = 'M',
            add_price     = 2300,
            quantity      = 10,
        )

        ProductOption.objects.create(
            id            = 4,
            product_id    = 1,
            option1_name  = 'color',
            option1_value = 'red',
            option2_name  = 'size',
            option2_value = 'L',
            add_price     = 2400,
            quantity      = 10,
        )

        Cycle.objects.create(
            id   = 1,
            hour = 6
        )

        PriceOption.objects.create(
            id          = 1,
            product_id  = 1,
            cycle_id    = 1,
            start_price = 10000,
            last_price  = 6000,
            start_at    = '2020-05-01 00:00:00',
            end_at      = '2020-05-02 00:00:00'
        )

        PriceData.objects.create(
            id              = 1,
            product_id      = 1,
            price_option_id = 1,
            cycle_id        = 1,
            discount_rate   = 0,
            discount_price  = 10000,
            is_active       = True,
            start_date      = '2020-05-01 00:00:00',
            end_date        = '2020-05-01 06:00:00'
        )

        PriceData.objects.create(
            id              = 2,
            product_id      = 1,
            price_option_id = 1,
            cycle_id        = 1,
            discount_rate   = 0.1,
            discount_price  = 9000,
            is_active       = False,
            start_date      = '2020-05-01 06:00:00',
            end_date        = '2020-05-01 12:00:00'
        )

        PriceData.objects.create(
            id              = 3,
            product_id      = 1,
            price_option_id = 1,
            cycle_id        = 1,
            discount_rate   = 0.2,
            discount_price  = 8000,
            is_active       = False,
            start_date      = '2020-05-01 12:00:00',
            end_date        = '2020-05-01 18:00:00'
        )

        PriceData.objects.create(
            id              = 4,
            product_id      = 1,
            price_option_id = 1,
            cycle_id        = 1,
            discount_rate   = 0.3,
            discount_price  = 7000,
            is_active       = False,
            start_date      = '2020-05-01 18:00:00',
            end_date        = '2020-05-02 00:00:00'
        )

    def test_product_detail_get_success(self):
        client   = Client()
        response = client.get('/product/detail/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {'data' : {
                'product' : {
                    'id' : 1,
                    'category_id' : 1,
                    'seller_id' : 1,
                    'name' : 'Gangwon-Do Potato',
                    'origin_price' : '10000.00',
                    'price' : '10000.00',
                    'stock' : 100,
                    'thumbnail_img' : 'url',
                    'description' : 'desc',
                    'delivery_fee' : '2500.00',
                    'is_option' : True
                },
                'option' : {
                    'color' : [
                        'black',
                        'red'
                    ],
                    'size' : [
                        'M',
                        'L'
                    ],
                    'null' : [
                        None
                    ]
                },
                'option_value' : [
                    ['2100.00', 10],
                    ['2200.00', 10],
                    ['2300.00', 10],
                    ['2400.00', 10]
                ],
                'seller' : {
                    'id' : 1,
                    'name' : 'Gangwon-Do'
                }
            }
        })

    def test_product_get_does_not_exist(self):
        client   = Client()
        response = client.get('/product/detail/0')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'PRODUCT_DOES_NOT_EXIST'
            }
        )

class ProductResistrationTest(TestCase):

    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = 'food'
        )

        Seller.objects.create(
            id    = 1,
            email = 'a@a.com',
            name  = 'seller'
        )

        Cycle.objects.create(
            id   = 1,
            hour = 6
        )


    def test_product_resgistration_post_success(self):
        client = Client()
        user   = Seller.objects.get(id=1)
        token  = jwt.encode({
            'email' : user.email},
            SECRET_KEY['secret'],
            algorithm = SECRET_KEY['algorithm']).decode('utf-8')
        data = {
            'product' : {
                'category_id' : 1,
                'name' : 'Gangwon-Do potato',
                'origin_price' : 19900,
                'stock' : 10,
                'thumbnail_img' : 'url',
                'description' : 'desc',
                'delivery_fee' : 2500,
                'is_option' : True
                },
            'product_option' : [
                ['color', 'black', 'size', 'M', None, None, 2100, 10],
                ['color', 'black', 'size', 'L', None, None, 2200, 10],
                ['color', 'red', 'size', 'M', None, None, 2300, 10],
                ['color', 'red', 'size', 'L', None, None, 2400, 10]
            ],
            'cycle_id' : 1,
            'price_option' : {
                'start_price' : 10000,
                'last_price' : 6000,
                'start_at' : '2020-05-01 00:00:00',
                'end_at' : '2020-05-02 00:00:00'
            },
        }
        response = client.post(
            '/product/registration',
            json.dumps(data),
            **{'HTTP_Authorization':token,
               'content_type' : 'application/json'
               }
        )
        self.assertEqual(response.status_code, 200)

class ProductModificationTest(TestCase):

    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = 'food'
        )

        Seller.objects.create(
            id    = 1,
            email = 'a@a.com',
            name  = 'seller'
        )

        SellerInfo.objects.create(
            id           = 1,
            seller_id    = 1,
            password     = 1234,
            company_name = 'Gangwon-Do'
        )

        Product.objects.create(
            id            = 1,
            category_id   = 1,
            seller_id     = 1,
            name          = 'Gangwon-Do potato',
            origin_price  = 19900,
            stock         = 100,
            thumbnail_img = 'url',
            description   = 'desc',
            delivery_fee  = 2500,
            is_option     = True
        )

        ProductOption.objects.create(
            id            = 1,
            product_id    = 1,
            option1_name  = 'color',
            option1_value = 'black',
            option2_name  = 'size',
            option2_value = 'M',
            add_price     = 2100,
            quantity      = 10,
        )

        ProductOption.objects.create(
            id            = 2,
            product_id    = 1,
            option1_name  = 'color',
            option1_value = 'black',
            option2_name  = 'size',
            option2_value = 'L',
            add_price     = 2200,
            quantity      = 10,
        )

        ProductOption.objects.create(
            id            = 3,
            product_id    = 1,
            option1_name  = 'color',
            option1_value = 'red',
            option2_name  = 'size',
            option2_value = 'M',
            add_price     = 2300,
            quantity      = 10,
        )

        ProductOption.objects.create(
            id            = 4,
            product_id    = 1,
            option1_name  = 'color',
            option1_value = 'red',
            option2_name  = 'size',
            option2_value = 'L',
            add_price     = 2400,
            quantity      = 10,
        )

        Cycle.objects.create(
            id   = 1,
            hour = 6
        )

        PriceOption.objects.create(
            id          = 1,
            product_id  = 1,
            cycle_id    = 1,
            start_price = 10000,
            last_price  = 6000,
            start_at    = '2020-05-01 00:00:00',
            end_at      = '2020-05-02 00:00:00'
        )

        PriceData.objects.create(
            id              = 1,
            product_id      = 1,
            price_option_id = 1,
            cycle_id        = 1,
            discount_rate   = 10,
            discount_price  = 9000,
            is_active       = True,
            start_date      = '2020-05-01 00:00:00',
            end_date        = '2020-05-01 06:00:00'
        )

        PriceData.objects.create(
            id              = 2,
            product_id      = 1,
            price_option_id = 1,
            cycle_id        = 1,
            discount_rate   = 20,
            discount_price  = 8000,
            is_active       = False,
            start_date      = '2020-05-01 06:00:00',
            end_date        = '2020-05-01 12:00:00'
        )

        PriceData.objects.create(
            id              = 3,
            product_id      = 1,
            price_option_id = 1,
            cycle_id        = 1,
            discount_rate   = 30,
            discount_price  = 7000,
            is_active       = False,
            start_date      = '2020-05-01 12:00:00',
            end_date        = '2020-05-01 18:00:00'
        )

        PriceData.objects.create(
            id              = 4,
            product_id      = 1,
            price_option_id = 1,
            cycle_id        = 1,
            discount_rate   = 40,
            discount_price  = 6000,
            is_active       = False,
            start_date      = '2020-05-01 18:00:00',
            end_date        = '2020-05-02 00:00:00'
        )

    def test_product_modification_post_success(self):
        client = Client()
        user   = Seller.objects.get(id=1)
        token  = jwt.encode({
            'email' : user.email},
            SECRET_KEY['secret'],
            algorithm = SECRET_KEY['algorithm']).decode('utf-8')
        data = {
            'product' : {
                'category_id' : 1,
                'name' : 'Gangwon-Do sweet potato',
                'origin_price' : 19900,
                'stock' : 10,
                'thumbnail_img' : 'url',
                'description' : 'desc',
                'delivery_fee' : 2500,
                'is_option' : True
                },
            'product_option' : [
                ['color', 'black', 'size', 'M', None, None, 2100, 10],
                ['color', 'black', 'size', 'L', None, None, 2200, 10],
                ['color', 'red', 'size', 'M', None, None, 2300, 10],
                ['color', 'red', 'size', 'L', None, None, 2400, 10]
            ],
            'cycle_id' : 1,
            'price_option' : {
                'start_price' : 10000,
                'last_price' : 6000,
                'start_at' : '2020-05-01 00:00:00',
                'end_at' : '2020-05-02 00:00:00'
            },
        }
        response = client.post(
            '/product/modification',
            json.dumps(data),
            **{'HTTP_Authorization':token,
               'content_type' : 'application/json'
               }
        )
        self.assertEqual(response.status_code, 200)
