from django.urls import path
from .views import BookStockView

urlpatterns = [
    # GET /api/books/<isbn>/stock/
    path('<str:isbn>/stock/', BookStockView.as_view(), name='book-stock'),
]
