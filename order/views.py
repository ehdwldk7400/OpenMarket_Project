import json

from account.utils   import Seller_Login_Check, Buyer_Login_Check
from product.models  import Category, Product, ProductOption, PriceData
from account.models  import Seller, SellerInfo, Buyer, BuyerInfo
from .models         import Cart, Order, OrderProduct, OrderProductOption, OrderStatus

from django.views  import View
from decimal       import Decimal
from django.http   import JsonResponse, HttpResponse
from django.db     import IntegrityError, transaction

class CartView(View):
    @Buyer_Login_Check
    def post(self, request):
        ''' cart 담기 '''
        try:
            data = json.loads(request.body)
            
            product_data  = data['product_id']
            quantity_data = data['quantity']

            # 상품 옵션 유무 확인
            if ProductOption.objects.filter(product_id=data['product_id']).exists():
                # 선택된 상품의 옵션 ID 값 검색
                product_option_data = ProductOption.objects.get(
                    product_id    = data['product_id'],
                    option1_name  = data['option_data']['option1_name'],
                    option1_value = data['option_data']['option1_value'],
                    option2_name  = data['option_data']['option2_name'],
                    option2_value = data['option_data']['option2_value'],
                    option3_name  = data['option_data']['option3_name'],
                    option3_value = data['option_data']['option3_value'],
                ).id

                # Cart에 담긴 상품에 대한 데이터 생성
                Cart.objects.create(
                    product_name      = Product.objects.get(id = product_data).name,
                    product_option_id = product_option_data,
                    quantity          = quantity_data,
                    buyer_id          = request.user,
                    product_id        = product_data          
                )

                return HttpResponse(status=200)

            else:
                Cart.objects.create(
                    product_name      = Product.objects.get(id = product_data).name,
                    quantity          = quantity_data,
                    buyer_id          = request.user,
                    product_id        = product_data          
                )         

        except KeyError:
            return HttpResponse(status=400)

    @Buyer_Login_Check
    def get(self, request):
        ''' cart 불러오기 '''
        cart_list = []
        for cart in Cart.objects.filter(buyer_id = request.user, is_deleted=False):
            print(cart)
            # 상품 옵션 유무에 판별
            if ProductOption.objects.filter(id=cart.product_option_id).exists():
                cart_data = {
                    'option_data' : {
                        'option_id'     : ProductOption.objects.get(id=cart.product_option_id).id,
                        'option1_name'  : ProductOption.objects.get(id=cart.product_option_id).option1_name,
                        'option1_value' : ProductOption.objects.get(id=cart.product_option_id).option1_value,
                        'option2_name'  : ProductOption.objects.get(id=cart.product_option_id).option2_name,
                        'option2_value' : ProductOption.objects.get(id=cart.product_option_id).option2_value,
                        'option3_name'  : ProductOption.objects.get(id=cart.product_option_id).option3_name,
                        'option3_value' : ProductOption.objects.get(id=cart.product_option_id).option3_value,
                        'add_price'     : ProductOption.objects.get(id=cart.product_option_id).add_price
                    },
                    'quantity'         : cart.quantity,
                    'thumbnail'        : Product.objects.get(id=cart.product_id).thumbnail_img,
                    'origin_price'     : Product.objects.get(id=cart.product_id).origin_price,
                    'product_name'     : cart.product_name,
                    'discount_percent' : PriceData.objects.get(product_id=cart.product_id, is_active=True).discount_rate,
                    'discount_price'   : PriceData.objects.get(product_id=cart.product_id, is_active=True).discount_price
                }
                cart_list.append(cart_data)
            else:
                cart_data = {
                    'option_data' : {
                        'option_id'     : None,
                        'option1_name'  : None,
                        'option1_value' : None,
                        'option2_name'  : None,
                        'option2_value' : None,
                        'option3_name'  : None,
                        'option3_value' : None,
                        'add_price'     : None
                    },
                    'quantity'         : cart.quantity,
                    'thumbnail'        : Product.objects.get(id=cart.product_id).thumbnail_img,
                    'origin_price'     : Product.objects.get(id=cart.product_id).origin_price,
                    'product_name'     : cart.product_name,
                    'discount_percent' : PriceData.objects.get(product_id=cart.product_id, is_active=True).discount_rate,
                    'discount_price'   : PriceData.objects.get(product_id=cart.product_id, is_active=True).discount_price
                }
                cart_list.append(cart_data)
                print(cart_list)
           
        return JsonResponse({'cart_data' : cart_list}, status=200)

class OrderView(View):
    @Buyer_Login_Check 
    def post(self, request):
        ''' 결제 후, Order 목록애 추가 '''
        try:
            with transaction.atomic():
                data = json.loads(request.body)

                total_amount = 0
                total_price  = Decimal(0)

                order = Order.objects.create(
                    buyer_id      = request.user,
                    receiver_name = data['receiver_name'],
                    order_amount  = len(data['cart_data'])
                )

                for index in range(0, len(data['cart_data'])):
                    cart_data      = Cart.objects.get(id=data['cart_data'][index]['cart_id'])
                    product_option = ProductOption.objects.get(id=cart_data.product_option_id)
                    
                    # 주문처리된 cart를 soft delete
                    cart = Cart.objects.filter(id=cart_data.id)
                    cart.update(
                        is_deleted = True,
                        is_buy     = True
                    )

                    # 주문 상품에 관한 데이터 생성
                    order_product = OrderProduct.objects.create(
                        seller_id       = cart_data.product.seller_id,
                        order_id        = order.id,
                        product_id      = cart_data.product_id,
                        order_status_id = OrderStatus.objects.get(id=1).id,
                        product_name    = cart_data.product_name,
                        origin_price    = cart_data.product.origin_price,
                        price           = PriceData.objects.get(product_id=cart_data.product_id, is_active=True).discount_price,
                        quantity        = cart_data.quantity,
                    )

                    # 상품 옵션 유무 판별
                    if ProductOption.objects.filter(id=cart_data.product_option_id).exists():
                        product_option = ProductOption.objects.get(id=cart_data.product_option_id)

                        # 주문 상품에 대한 옵션 데이터 생성
                        OrderProductOption.objects.create(
                            order_product_id  = order_product.id,
                            product_option_id = cart_data.product_option_id,
                            option1_name      = product_option.option1_name,
                            option1_value     = product_option.option1_value,
                            option2_name      = product_option.option2_name,
                            option2_value     = product_option.option2_value,
                            option3_name      = product_option.option3_name,
                            option3_value     = product_option.option3_value,
                            add_price         = product_option.add_price
                        )

                    # 주문한 상품 총 수량, 총 가격 계산
                    total_amount += cart_data.quantity
                    total_price  += PriceData.objects.get(product_id=cart_data.product_id, is_active=True).discount_price

                # 계산된 total_amount, total_price 데이터 order 테이블에 추가
                order.total_amount = total_amount
                order.total_price  = total_price
                order.save()

                return HttpResponse(status=200)
            
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status=400)

    @Buyer_Login_Check
    def get(self, request):
        ''' Order 목록 조회 '''

        order_list = []
        # 구매자 ID에 등록되어 있는order 목록 조회
        for order in Order.objects.filter(buyer_id=request.user):

            # 각 order에 존재하는 상품 검색
            for order_product in OrderProduct.objects.filter(order_id=order.id):

                # 상품 옵션 유무 확인
                if OrderProductOption.objects.filter(order_product_id=order_product.id).exists():
                    order_data = {
                        'order_amount' : order.order_amount,
                        'total_amount' : order.total_amount,
                        'total_price'  : order.total_price,
                        'price_data'   : {
                            'product_name' : order_product.product_name,
                            'order_status' : order_product.order_status.name,
                            'origin_price' : order_product.origin_price,
                            'price'        : order_product.price,
                            'quantity'     : order_product.quantity,
                            'option_data'  : {
                                'option1_name'  : OrderProductOption.objects.get(order_product_id=order_product.id).option1_name,
                                'option1_value' : OrderProductOption.objects.get(order_product_id=order_product.id).option1_value,
                                'option2_name'  : OrderProductOption.objects.get(order_product_id=order_product.id).option2_name,
                                'option2_value' : OrderProductOption.objects.get(order_product_id=order_product.id).option2_value,
                                'option3_name'  : OrderProductOption.objects.get(order_product_id=order_product.id).option3_name,
                                'option3_value' : OrderProductOption.objects.get(order_product_id=order_product.id).option3_value,
                                'add_price'     : OrderProductOption.objects.get(order_product_id=order_product.id).add_price
                            }    
                        }
                    }
                    order_list.append(order_data)

                else:
                    order_data = {
                        'order_amount' : order.order_amount,
                        'total_amount' : order.total_amount,
                        'total_price'  : order.total_price,
                        'price_data'   : {
                            'product_name' : order_product.product_name,
                            'order_status' : order_product.order_status.name,
                            'origin_price' : order_product.origin_price,
                            'price'        : order_product.price,
                            'quantity'     : order_product.quantity,
                            'option_data'  : {
                                'option1_name'  : None,
                                'option1_value' : None,
                                'option2_name'  : None,
                                'option2_value' : None,
                                'option3_name'  : None,
                                'option3_value' : None,
                                'add_price'     : None,
                            }    
                        }
                    }
                    order_list.append(order_data)
                    print(order_list)
        return JsonResponse({'order_data' : order_list}, status=200)
