from django.urls import path
from .views      import CartView, OrderView


urlpatterns = [
    path('', OrderView.as_view()),
    path('/cart', CartView.as_view()),    
]
