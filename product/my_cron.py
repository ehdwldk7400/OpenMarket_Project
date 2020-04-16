from product.models import Product, PriceData, Cycle
from django.db      import IntegrityError, transaction

def schedule_24hr_change_price():
    ''' 가격 변동 주기가 24시간 상품에 대하여 가격 변경 수행'''
    try:
        with transaction.atomic():

            # product_list : 가격 변경 대상인 상품, 리스트에 추가
            product_list = []             
            cycle = 24

            # 현재 적용되어 있는 가격 정책 비활성화
            for price in PriceData.objects.filter(cycle__hour = cycle, is_active=True):
                product_list.append(price.product_id)
                price.is_active  = False
                price.is_deleted = True
                price.save()

            # 다음 가격 정책 활성화
            for product in product_list:
                if PriceData.objects.filter(product_id = product, cycle__hour = cycle, is_deleted = False, is_active = False).exists():
                    element = PriceData.objects.filter(product_id = product, cycle__hour = cycle, is_deleted = False, is_active = False).order_by('start_date')[0]
                    element.is_active = True
                    element.save() 
                else:
                    element = Product.objects.get(id = product)
                    element.is_active = False
                    element.save()
            
            print('24hr_SUCCESS')
                
    except IntegrityError:
        return JsonResponse({"message":"Try again"}, status = 400) 

def schedule_12hr_change_price():
    ''' 가격 변동 주기가 12시간 상품에 대하여 가격 변경 수행'''
    try:
        with transaction.atomic():

            # product_list : 가격 변경 대상인 상품, 리스트에 추가
            # cycle_list   : 변경할 가격 주기 데이터, 리스트에 추가
            product_list = []   
            cycle = 12  


            # 현재 적용되어 있는 가격 정책 비활성화
            for price in PriceData.objects.filter(cycle__hour = cycle, is_active=True):
                product_list.append(price.product_id)
                price.is_active  = False
                price.is_deleted = True
                price.save()

            # 다음 가격 정책 활성화
            for product in product_list:
                if PriceData.objects.filter(product_id = product, cycle__hour = cycle, is_deleted = False, is_active = False).exists():
                    element = PriceData.objects.filter(product_id = product, cycle__hour = cycle, is_deleted = False, is_active = False).order_by('start_date')[0]
                    element.is_active = True
                    element.save() 
                else:
                    element = Product.objects.get(id = product)
                    element.is_active = False
                    element.save()
            print('12hr_SUCCESS')
                
    except IntegrityError:
        return JsonResponse({"message":"Try again"}, status = 400) 

def schedule_06hr_change_price():
    ''' 가격 변동 주기가 06시간 상품에 대하여 가격 변경 수행'''
    try:
        with transaction.atomic():

            # product_list : 가격 변경 대상인 상품, 리스트에 추가
            product_list = []
            cycle = 6

            # 현재 적용되어 있는 가격 정책 비활성화
            for price in PriceData.objects.filter(cycle__hour = cycle, is_active=True):
                product_list.append(price.product_id)
                price.is_active  = False
                price.is_deleted = True
                price.save()

            # 다음 가격 정책 활성화
            for product in product_list:
                if PriceData.objects.filter(product_id = product, cycle__hour = cycle, is_deleted = False, is_active = False).exists():
                    element = PriceData.objects.filter(product_id = product, cycle__hour = cycle, is_deleted = False, is_active = False).order_by('start_date')[0]
                    element.is_active = True
                    element.save() 
                else:
                    element = Product.objects.get(id = product)
                    element.is_active = False
                    element.save()
            
            print('06hr_SUCCESS')
                
    except IntegrityError:
        return JsonResponse({"message":"Try again"}, status = 400)      

def schedule_03hr_change_price():
    ''' 가격 변동 주기가 03시간 상품에 대하여 가격 변경 수행'''
    try:
        with transaction.atomic():
            # 가격 변경 대상인 상품, 리스트에 추가
            product_list = []
            cycle = 3

            # 현재 적용되어 있는 가격 정책 비활성화
            for price in PriceData.objects.filter(cycle__hour = cycle, is_active=True):
                product_list.append(price.product_id)
                price.is_active  = False
                price.is_deleted = True
                price.save()

            # 다음 가격 정책 활성화
            for product in product_list:
                if PriceData.objects.filter(product_id = product, cycle__hour = cycle, is_deleted = False, is_active = False).exists():
                    element = PriceData.objects.filter(product_id = product, cycle__hour = cycle, is_deleted = False, is_active = False).order_by('start_date')[0]
                    element.is_active = True
                    element.save() 
                else:
                    element = Product.objects.get(id = product)
                    element.is_active = False
                    element.save()
                
            print('03hr_SUCCESS')

    except IntegrityError:
        return JsonResponse({"message":"Try again"}, status = 400)       


