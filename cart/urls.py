from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cart_index'),
    path('add/<int:id>/', views.add, name='cart_add'),
    path('clear/', views.clear, name='cart_clear'),
    path('purchase/', views.purchase, name='cart_purchase'),

    # NEW success page that launches the modal
    path('success/<int:order_id>/', views.purchase_success, name='cart_purchase_success'),

    # Existing feedback routes
    path('survey/<int:order_id>/', views.survey, name='cart_survey'),
    path('survey/thanks/', views.survey_thanks, name='cart_survey_thanks'),
    path('surveys/', views.survey_list, name='cart_survey_list'),
]


