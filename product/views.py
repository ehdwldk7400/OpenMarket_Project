import json
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from account.utils  import Seller_Login_Check
from account.models import SellerInfo
from .models import(
    Product,
    ProductOption,
    PriceData,
    PriceOption,
    Cycle,
)

from django.views import View
from django.http import HttpResponse, JsonResponse

# 상품 등록
class ProductRegistrationView(View):
    @Seller_Login_Check
    def post(self, request):
        try:
            data         = json.loads(request.body)
            seller_id    = request.user
            origin_price = data['product']['origin_price']
            start_price  = data['price_option']['start_price']
            last_price   = data['price_option']['last_price']
            start_at     = data['price_option']['start_at']
            end_at       = data['price_option']['end_at']

            # 상품 정보 저장
            product = Product(
                category_id   = data['product']['category_id'],
                seller_id     = seller_id,
                name          = data['product']['name'],
                origin_price  = origin_price,
                stock         = data['product']['stock'],
                thumbnail_img = data['product']['thumbnail_img'],
                description   = data['product']['description'],
                delivery_fee  = data['product']['delivery_fee'],
                is_option     = data['product']['is_option']
            )
            product.save()

            # 옵션 정보 저장
            if product.is_option:
                product_option_list = []
                len_product_option = len(data['product_option'])
                for n in range(len_product_option):
                    product_option_list.append(ProductOption(
                        product_id    = product.id,
                        option1_name  = data['product_option'][n][0],
                        option1_value = data['product_option'][n][1],
                        option2_name  = data['product_option'][n][2],
                        option2_value = data['product_option'][n][3],
                        option3_name  = data['product_option'][n][4],
                        option3_value = data['product_option'][n][5],
                        add_price     = data['product_option'][n][6],
                        quantity      = data['product_option'][n][7]
                    ))
                ProductOption.objects.bulk_create(product_option_list)

            # 가격 옵션 저장
            price_option = PriceOption(
                product_id  = product.id,
                cycle_id    = data['cycle_id'],
                start_price = start_price,
                last_price  = last_price,
                start_at    = start_at,
                end_at      = end_at
            )
            price_option.save()

            # 가격 정보 저장
            start       = datetime.datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S')
            end         = datetime.datetime.strptime(end_at, '%Y-%m-%d %H:%M:%S')
            cycle_hour  = Cycle.objects.get(id=data['cycle_id']).hour
            diff        = end - start
            total_hours = int(diff.total_seconds())//3600
            cycle       = total_hours // Cycle.objects.get(id=data['cycle_id']).hour
            price_data_list = []
            for n in range(cycle):
                discount_amount = int(start_price) - int(last_price)
                discount_price  = int(start_price) - discount_amount/cycle * n
                discount_rate   = 1 - discount_price/int(origin_price)
                start_date      = start + timedelta(hours=n * cycle_hour)
                end_date        = start_date + timedelta(hours=cycle_hour)
                price_data_list.append(PriceData(
                    product_id      = product.id,
                    price_option_id = price_option.id,
                    cycle_id        = data['cycle_id'],
                    discount_price  = discount_price,
                    discount_rate   = discount_rate,
                    start_date      = start_date,
                    end_date        = end_date
                ))

            # 첫번째 순서인 가격 활성화
            first_price = price_data_list[0]
            first_price.is_active = True

            PriceData.objects.bulk_create(price_data_list)

            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status = 400)


# 상품 수정
class ProductEditView(View):
    @Seller_Login_Check
    def get(self, request, product_id):
        product = Product.objects.filter(id = product_id).values()
        print(product[0])
        if product[0]["is_option"]:
            product_option = ProductOption.objects.filter(product_id=product_id).values()
            price_option = PriceOption.objects.filter(product_id=product_id).values()
            price_data = PriceData.objects.filter(product_id=product_id, is_deleted=False).values()

            return JsonResponse({
                "data" : {
                    "product" : product[0],
                    "product_option" : product_option[0],
                    "price_option" : price_option[0],
                    "price_data" : price_data[0]
                }
            }, status = 200)

        else:
            price_option = PriceOption.objects.filter(product_id=product_id).values()
            price_data = PriceData.objects.filter(product_id=product_id, is_deleted=False).values()

            return JsonResponse({
                "data" : {
                    "product" : product[0],
                    "product_option" : [],
                    "price_option" : price_option[0],
                    "price_data" : price_data[0]
                }
            }, status = 200)


    @Seller_Login_Check
    def post(self, request, product_id):
        try:
            data         = json.loads(request.body)
            product      = Product.objects.get(id=product_id)
            origin_price = data['product']['origin_price']
            start_price  = data['price_option']['start_price']
            last_price   = data['price_option']['last_price']
            start_at     = data['price_option']['start_at']
            end_at       = data['price_option']['end_at']

            # 상품 정보 업데이트
            product_info = Product.objects.filter(id = product_id).values()
            product_info.update(
                category_id   = data['product']['category_id'],
                name          = data['product']['name'],
                origin_price  = origin_price,
                stock         = data['product']['stock'],
                thumbnail_img = data['product']['thumbnail_img'],
                description   = data['product']['description'],
                delivery_fee  = data['product']['delivery_fee'],
                is_option     = data['product']['is_option']
            )

            # 옵션 정보 업데이트
            product_option = ProductOption.objects.filter(product_id = product_id)
            if product.is_option:
                for p in product_option:
                    p.is_active = False

            if data['product']['is_option']:
                product_option_list = []
                len_product_option = len(data['product_option'])
                for n in range(len_product_option):
                    product_option_list.append(ProductOption(
                        product_id    = product_id,
                        option1_name  = data['product_option'][n][0],
                        option1_value = data['product_option'][n][1],
                        option2_name  = data['product_option'][n][2],
                        option2_value = data['product_option'][n][3],
                        option3_name  = data['product_option'][n][4],
                        option3_value = data['product_option'][n][5],
                        add_price     = data['product_option'][n][6],
                        quantity      = data['product_option'][n][7]
                    ))
                ProductOption.objects.bulk_create(product_option_list)

            # 가격 옵션 업데이트
            price_option = PriceOption.objects.filter(product_id=product_id)
            price_option.update(
                cycle_id    = data['cycle_id'],
                start_price = start_price,
                last_price  = last_price,
                start_at    = start_at,
                end_at      = end_at
            )

            # 가격 정보 저장
            ## 기존 가격 정보 비활성
            price_data = PriceData.objects.filter(product_id=product_id, is_deleted = False)
            for p in price_data:
                p.is_deleted = True
                p.is_active = False

            start       = datetime.datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S')
            end         = datetime.datetime.strptime(end_at, '%Y-%m-%d %H:%M:%S')
            cycle_hour  = Cycle.objects.get(id=data['cycle_id']).hour
            total_hours = relativedelta(start, end).hours
            cycle       = total_hours // Cycle.objects.get(id=data['cycle_id']).hour
            price_data_list = []
            for n in range(cycle):
                discount_price  = start_price - n *((start_price - last_price)/cycle),
                discount_rate   = 1 - (discount_price/origin_price),
                start_date      = start + (n * cycle_hour),
                end_date        = start_date + timedelta(hours=cycle_hour)
                price_data_list.append(PriceData(
                    product_id      = product_id,
                    price_option_id = price_option.id,
                    cycle_id        = data['cycle_id'],
                    discount_price  = discount_price,
                    discount_rate   = discount_rate,
                    start_date      = start_date,
                    end_date        = end_date
                ))
            PriceData.objects.bulk_create(price_data_list)

            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status = 400)

# 상품 상세
class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            price   = PriceData.objects.get(product_id=product, is_active=True).discount_price

            # 옵션이 있는 경우
            if product.is_option:
                option  = ProductOption.objects.filter(product_id = product_id)
                option1 = option.values_list('option1_name', flat=True).distinct()[0]
                option2 = option.values_list('option2_name', flat=True).distinct()[0]
                option3 = option.values_list('option3_name', flat=True).distinct()[0]
                data    = {
                    'product' : {
                        'id'            : product.id,
                        'category_id'   : product.category_id,
                        'seller_id'     : product.seller_id,
                        'name'          : product.name,
                        'origin_price'  : product.origin_price,
                        'price'         : price,
                        'stock'         : product.stock,
                        'thumbnail_img' : product.thumbnail_img,
                        'description'   : product.description,
                        'delivery_fee'  : product.delivery_fee,
                        'is_option'     : product.is_option
                    },
                    'option' : {
                        option1 : list(option.values_list('option1_value', flat=True).distinct()),
                        option2 : list(option.values_list('option2_value', flat=True).distinct()),
                        option3 : list(option.values_list('option3_value', flat=True).distinct())
                    },
                    'option_value' : [
                        list(option)
                    for option in option.values_list('add_price', 'quantity')],
                    'seller' : {
                        'id' : SellerInfo.objects.get(id=product.seller_id).id,
                        'name' : SellerInfo.objects.get(id=product.seller_id).company_name
                    }
                }
                return JsonResponse({'data' : data}, status = 200)

            # 옵션이 없는 경우
            else:
                data    = {
                    'product' : {
                        'id'            : product.id,
                        'category_id'   : product.category_id,
                        'seller_id'     : product.seller_id,
                        'name'          : product.name,
                        'origin_price'  : product.origin_price,
                        'price'         : price,
                        'stock'         : product.stock,
                        'thumbnail_img' : product.thumbnail_img,
                        'description'   : product.description,
                        'delivery_fee'  : product.delivery_fee,
                        'is_option'     : product.is_option
                    },
                    'option' : {
                    },
                    'option_value' : [],
                    'seller' : {
                        'id' : SellerInfo.objects.get(id=product.seller_id).id,
                        'name' : SellerInfo.objects.get(id=product.seller_id).company_name
                    }
                }
                return JsonResponse({'data' : data}, status = 200)

        except PriceData.DoesNotExist:
            return JsonResponse({'message' : 'PRICE_DATA_DOES_NOT_EXIST'}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 400)
