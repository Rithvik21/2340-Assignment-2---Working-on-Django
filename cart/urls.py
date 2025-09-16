from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cart_index'),
    path('add/<int:id>/', views.add, name='cart_add'),
    path('clear/', views.clear, name='cart_clear'),
    path('purchase/', views.purchase, name='cart_purchase'),
]

