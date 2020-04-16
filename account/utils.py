import jwt
import json

from .models      import Seller, Buyer, SellerInfo, BuyerInfo
from my_settings  import SECRET_KEY

from django.http  import JsonResponse,HttpResponse

class Seller_Login_Check:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY["secret"], SECRET_KEY["algorithm"])
                user          = Seller.objects.get(email = token_payload["email"]).id
                request.user  = user

                return self.original_function(self, request, *args, **kwargs)

            return JsonResponse({"messaege":"NEED_LOGIN"}, status=401)

        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_USER"}, status=401)


class Buyer_Login_Check:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY["secret"], SECRET_KEY["algorithm"])
                user          = Buyer.objects.get(email = token_payload["email"]).id
                request.user  = user

                return self.original_function(self, request, *args, **kwargs)

            return JsonResponse({"messaege":"NEED_LOGIN"}, status=401)

        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_USER"}, status=401)