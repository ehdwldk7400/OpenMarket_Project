import jwt
import json
import bcrypt

from my_settings    import SECRET_KEY
from account.models import Buyer, BuyerInfo, Seller, SellerInfo
from product.models import Category, Product, ProductOption, PriceOption, Cycle, PriceData
from order.models   import Cart, Order, OrderProduct, OrderProductOption, OrderStatus

from django.test    import TestCase, Client


class CartView(TestCase):
    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = 'main'
        )

        Seller.objects.create(
            id    = 1,
            email = 'a@a.com',
            name  = 'seller'
        )

        SellerInfo.objects.create(
            id = 1,
            seller_id = 1,
            password = 1234,
            company_name = '강원도'
        )

        Buyer.objects.create(
            id    = 1,
            email = 'aaaa@aaa.com',
            name  = 'buyer'
        )

        BuyerInfo.objects.create(
            id       = 1,
            buyer_id = 1,
            password = bcrypt.hashpw("Test12341234!".encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
        )

        Product.objects.create(
            id               = 1,
            category_id      = 1,
            seller_id        = 1,
            name             = '강원도 감자',
            origin_price     = 19900.00,
            stock            = 100,
            delivery_fee     = 2500.00,
            thumbnail_img    = 'url',
            description      = 'desc'
        )

        ProductOption.objects.create(
            id             = 1,
            product_id     = 1,
            option1_name   = '색상',
            option1_value  = '검정',
            option2_name   = '사이즈',
            option2_value  = 'M',
            add_price      = 2100,
            quantity       = 10,
        )

        ProductOption.objects.create(
            id             = 2,
            product_id     = 1,
            option1_name   = '색상',
            option1_value  = '검정',
            option2_name   = '사이즈',
            option2_value  = 'L',
            add_price      = 2200,
            quantity       = 10,
        )

        ProductOption.objects.create(
            id             = 3,
            product_id     = 1,
            option1_name   = '색상',
            option1_value  = '빨강',
            option2_name   = '사이즈',
            option2_value  = 'M',
            add_price      = 2300,
            quantity       = 10,
        )

        ProductOption.objects.create(
            id             = 4,
            product_id     = 1,
            option1_name   = '색상',
            option1_value  = '빨강',
            option2_name   = '사이즈',
            option2_value  = 'L',
            add_price      = 2400,
            quantity       = 10,
        )

        Cycle.objects.create(
            id   = 1,
            hour = 6
        )

        PriceOption.objects.create(
            id          = 1,
            product_id  = 1,
            cycle_id    = 1,
            start_price = 10000.00,
            last_price  = 6000.00,
            start_at    = '2020-05-01 00:00:00',
            end_at      = '2020-05-01 23:59:59'
        )

        PriceData.objects.create(
            id               = 1,
            product_id       = 1,
            price_option_id  = 1,
            cycle_id         = 1,
            discount_rate    = 10,
            discount_price   = 9000.00,
            is_active        = True,
            start_date       = '2020-05-01 00:00:00',
            end_date         = '2020-05-01 05:59:59'
        )

        PriceData.objects.create(
            id               = 2,
            product_id       = 1,
            price_option_id  = 1,
            cycle_id         = 1,
            discount_rate    = 20,
            discount_price   = 8000.00,
            is_active        = False,
            start_date       = '2020-05-01 06:00:00',
            end_date         = '2020-05-01 11:59:59'
        )

        PriceData.objects.create(
            id               = 3,
            product_id       = 1,
            price_option_id  = 1,
            cycle_id         = 1,
            discount_rate    = 30,
            discount_price   = 7000.00,
            is_active        = False,
            start_date       = '2020-05-01 12:00:00',
            end_date         = '2020-05-01 17:59:59'
        )

        PriceData.objects.create(
            id               = 4,
            product_id       = 1,
            price_option_id  = 1,
            cycle_id         = 1,
            discount_rate    = 40,
            discount_price   = 6000.00,
            is_active        = False,
            start_date       = '2020-05-01 18:00:00',
            end_date         = '2020-05-01 23:59:59'
        )

        Cart.objects.create(
            id                = 1,
            product_option_id = 1,
            buyer_id          = 1,
            product_id        = 1,
            quantity          = 1,
            product_name      = '강원도 감자'
        )

    def test_create_cart_success(self):
        client   = Client()
        user     = Buyer.objects.get(id=1)
        token    = jwt.encode({"email" : user.email}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")
        data     = {
            'product_id'  : 1, 
            'quantity'    : 1,
            'option_data' : {
                'option1_name'  : '색상',
                'option1_value' : '검정',
                'option2_name'  : '사이즈',
                'option2_value' : 'M',
                'option3_name'  : None,
                'option3_value' : None

            }

        }
        response = client.post('/order/cart', json.dumps(data), **{'HTTP_Authorization':token, 'content_type' : 'applications/json'})

        self.assertEqual(response.status_code, 200)

    def test_create_cart_key_error(self):
        client   = Client()
        user     = Buyer.objects.get(id=1)
        token    = jwt.encode({"email" : user.email}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")
        data     = {
            'product'   : 1,         
        }

        response = client.post('/order/cart', json.dumps(data), **{'HTTP_Authorization':token, 'content_type' : 'applications/json'})
        
        self.assertEqual(response.status_code, 400)

    def test_read_cart_success(self):
        client   = Client()
        user     = Buyer.objects.get(id=1)
        token    = jwt.encode({"email" : user.email}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")
        response = client.get('/order/cart', **{'HTTP_Authorization':token, 'content_type' : 'applications/json'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'cart_data' : [
                    {
                        'option_data' : {
                            'option_id'     : 1,
                            'option1_name'  : '색상',
                            'option1_value' : '검정',
                            'option2_name'  : '사이즈',
                            'option2_value' : 'M',
                            'option3_name'  : None,
                            'option3_value' : None,
                            'add_price'     : '2100.00'
                        },
                        'quantity'         : 1,
                        'thumbnail'        : 'url',
                        'origin_price'     : '19900.00',
                        'product_name'     : '강원도 감자',
                        'discount_percent' : 10.0,
                        'discount_price'   : '9000.00'
                    }
                ]
            }
        )


class OrderView(TestCase):
    def setUp(self):
        Category.objects.create(
            id   = 1,
            name = 'main'
        )

        Seller.objects.create(
            id    = 1,
            email = 'a@a.com',
            name  = 'seller'
        )

        SellerInfo.objects.create(
            id = 1,
            seller_id = 1,
            password = 1234,
            company_name = '강원도'
        )

        Buyer.objects.create(
            id    = 1,
            email = 'aaaa@aaa.com',
            name  = 'buyer'
        )

        BuyerInfo.objects.create(
            id       = 1,
            buyer_id = 1,
            password = bcrypt.hashpw("Test12341234!".encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
        )

        Product.objects.create(
            id               = 1,
            category_id      = 1,
            seller_id        = 1,
            name             = '강원도 감자',
            origin_price     = 19900.00,
            stock            = 100,
            delivery_fee     = 2500.00,
            thumbnail_img    = 'url',
            description      = 'desc'
        )

        ProductOption.objects.create(
            id             = 1,
            product_id     = 1,
            option1_name   = '색상',
            option1_value  = '검정',
            option2_name   = '사이즈',
            option2_value  = 'M',
            add_price      = 2100,
            quantity       = 10,
        )

        ProductOption.objects.create(
            id             = 2,
            product_id     = 1,
            option1_name   = '색상',
            option1_value  = '검정',
            option2_name   = '사이즈',
            option2_value  = 'L',
            add_price      = 2200,
            quantity       = 10,
        )

        ProductOption.objects.create(
            id             = 3,
            product_id     = 1,
            option1_name   = '색상',
            option1_value  = '빨강',
            option2_name   = '사이즈',
            option2_value  = 'M',
            add_price      = 2300,
            quantity       = 10,
        )

        ProductOption.objects.create(
            id             = 4,
            product_id     = 1,
            option1_name   = '색상',
            option1_value  = '빨강',
            option2_name   = '사이즈',
            option2_value  = 'L',
            add_price      = 2400,
            quantity       = 10,
        )

        Cycle.objects.create(
            id   = 1,
            hour = 6
        )

        PriceOption.objects.create(
            id          = 1,
            product_id  = 1,
            cycle_id    = 1,
            start_price = 10000.00,
            last_price  = 6000.00,
            start_at    = '2020-05-01 00:00:00',
            end_at      = '2020-05-01 23:59:59'
        )

        PriceData.objects.create(
            id               = 1,
            product_id       = 1,
            price_option_id  = 1,
            cycle_id         = 1,
            discount_rate    = 10,
            discount_price   = 9000.00,
            is_active        = True,
            start_date       = '2020-05-01 00:00:00',
            end_date         = '2020-05-01 05:59:59'
        )

        PriceData.objects.create(
            id               = 2,
            product_id       = 1,
            price_option_id  = 1,
            cycle_id         = 1,
            discount_rate    = 20,
            discount_price   = 8000.00,
            is_active        = False,
            start_date       = '2020-05-01 06:00:00',
            end_date         = '2020-05-01 11:59:59'
        )

        PriceData.objects.create(
            id               = 3,
            product_id       = 1,
            price_option_id  = 1,
            cycle_id         = 1,
            discount_rate    = 30,
            discount_price   = 7000.00,
            is_active        = False,
            start_date       = '2020-05-01 12:00:00',
            end_date         = '2020-05-01 17:59:59'
        )

        PriceData.objects.create(
            id               = 4,
            product_id       = 1,
            price_option_id  = 1,
            cycle_id         = 1,
            discount_rate    = 40,
            discount_price   = 6000.00,
            is_active        = False,
            start_date       = '2020-05-01 18:00:00',
            end_date         = '2020-05-01 23:59:59'
        )

        Cart.objects.create(
            id                = 1,
            product_option_id = 1,
            buyer_id          = 1,
            product_id        = 1,
            quantity          = 1,
            product_name      = '강원도 감자'
        )

        OrderStatus.objects.create(
            id   = 1,
            name = '결제 완료'
        )

        Order.objects.create(
            id            = 1,
            buyer_id      = 1,
            receiver_name = 'kim',
            order_amount  = 1,
            total_amount  = 1,
            total_price   = '1.00'
        )

        OrderProduct.objects.create(
            id              = 1,
            order_id        = 1,
            seller_id       = 1,
            product_id      = 1,
            order_status_id = 1,
            product_name    = '강원도 감자',
            origin_price    = '19900.00',
            price           = '9000.00',
            quantity        = 1
        )

        OrderProductOption.objects.create(
            order_product_id  = 1,
            product_option_id = 1,
            option1_name      = '색상',
            option1_value     = '검정',
            option2_name      = '사이즈',
            option2_value     = 'M',
            option3_name      = None,
            option3_value     = None,
            add_price         = '2100.00'
        )

    def test_create_order_success(self):
        client   = Client()
        user     = Buyer.objects.get(id=1)
        token    = jwt.encode({"email" : user.email}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")
        data     = {
            'receiver_name' : 'kim',
            'cart_data'     : [
                {
                    'cart_id' : 1
                }]
            }

        response = client.post('/order', json.dumps(data), **{'HTTP_Authorization':token, 'content_type' : 'applications/json'})
 
        self.assertEqual(response.status_code, 200)
     
    def test_read_order_success(self):
        client   = Client()
        user     = Buyer.objects.get(id=1)
        token    = jwt.encode({"email" : user.email}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")
        response = client.get('/order', **{'HTTP_Authorization':token, 'content_type' : 'applications/json'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'order_data' : [
                    {
                        'order_amount' : 1,
                        'total_amount' : 1,
                        'total_price'  : '1.00',
                        'price_data'   : {
                            'product_name' : '강원도 감자',
                            'order_status' : '결제 완료',
                            'origin_price' : '19900.00',
                            'price'        : '9000.00',
                            'quantity'     : 1,
                            'option_data'  : {
                                'option1_name'  : '색상',
                                'option1_value' : '검정',
                                'option2_name'  : '사이즈',
                                'option2_value' : 'M',
                                'option3_name'  : None,
                                'option3_value' : None,
                                'add_price'     : '2100.00'
                            }
                        }
                    }
                ]
            }    
        )
  
  
  
  