import json
import bcrypt
import jwt

from .models       import Seller, Buyer, SellerInfo, BuyerInfo
from .utils        import Seller_Login_Check, Buyer_Login_Check
from my_settings   import SECRET_KEY

from django.views            import View
from django.http             import HttpResponse, JsonResponse
from django.db               import IntegrityError
from django.core.validators  import validate_email
from django.core.exceptions  import ValidationError
from django.db               import IntegrityError, transaction


class SellerSignUp(View):
    def post(self, request):
        ''' 판매자 회원 가입 '''
        try:
            with transaction.atomic():

                data = json.loads(request.body)
                validate_email(data['email'])

                if Buyer.objects.filter(email=data['email']).exists() and Seller.objects.filter(email=data['email']).exists():
                    return JsonResponse({'message' : 'EXISTS_EMAIL'}, status=400)

                user = Seller.objects.create(
                    name  = data['name'],
                    email = data['email'],
                )

                SellerInfo.objects.create(
                    seller_id      = user.id,
                    password       = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8'),
                    company_name   = data['company_name'],
                    company_type   = data['company_type'],
                    company_number = data['company_number'],
                    address        = data['address'],
                    phone_number   = data['phone_number'],
                    bank_account   = data['bank_account'],
                )

                return HttpResponse(status=200)

        except ValidationError:
            return JsonResponse({'message' : 'VALIDATION_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)


class BuyerSignUp(View):
    def post(self, request):
        ''' 구매자 회원 가입 '''
        try:
            with transaction.atomic():

                data = json.loads(request.body)
                validate_email(data['email'])

                if Buyer.objects.filter(email=data['email']).exists() and Seller.objects.filter(email=data['email']).exists():
                    return JsonResponse({'message' : 'EXISTS_EMAIL'}, status=400)

                user = Buyer.objects.create(
                    name  = data['name'],
                    email = data['email'],
                )

                BuyerInfo.objects.create(
                    buyer_id    = user.id,
                    password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
                )

                return HttpResponse(status=200)

        except ValidationError:
            return JsonResponse({'message' : 'VALIDATION_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)


class SellerSignIn(View):
    def post(self, request):
        ''' 판매자 로그인 '''
        try:
            data = json.loads(request.body)
            validate_email(data["email"])

            if Seller.objects.filter(email=data["email"]).exists():
                seller_account = Seller.objects.get(email=data["email"])
                user = SellerInfo.objects.get(seller_id=seller_account.id)

                if bcrypt.checkpw(data["password"].encode(), user.password.encode("UTF-8")):
                    token = jwt.encode({"email" : data["email"]}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")

                    return JsonResponse({"Authorization" : token}, status=200)

                return HttpResponse(status=401)

            return JsonResponse({"message" : "NOT_EXISTS_MAIL"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)


class BuyerSignIn(View):
    def post(self, request):
        ''' 구매자 로그인 '''
        try:
            data = json.loads(request.body)
            validate_email(data["email"])

            if Buyer.objects.filter(email=data["email"]).exists():
                buyer_account = Buyer.objects.get(email=data["email"])
                user = BuyerInfo.objects.get(buyer_id=buyer_account.id)

                if bcrypt.checkpw(data["password"].encode(), user.password.encode("UTF-8")):
                    token = jwt.encode({"email" : data["email"]}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")

                    return JsonResponse({"Authorization" : token}, status=200)

                return HttpResponse(status=401)

            return JsonResponse({"message" : "NOT_EXISTS_MAIL"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)
