from django.urls import path
from .views      import SellerSignUp, SellerSignIn, BuyerSignUp, BuyerSignIn

urlpatterns = [
    path('/seller/signup', SellerSignUp.as_view()),
    path('/seller/signin', SellerSignIn.as_view()),
    path('/buyer/signup', BuyerSignUp.as_view()),
    path('/buyer/signin', BuyerSignIn.as_view()),
]