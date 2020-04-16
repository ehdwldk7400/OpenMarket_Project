from django.urls import path

from .views import (
    ProductDetailView,
    ProductRegistrationView,
    ProductEditView
)

urlpatterns = [
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
    path('/registration', ProductRegistrationView.as_view()),
    path('/edit/<int:product_id>', ProductEditView.as_view()),
]
