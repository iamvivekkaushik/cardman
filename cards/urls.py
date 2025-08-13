from django.urls import path

from .views import *

urlpatterns = [
    path('add/', CardAddView.as_view(), name='card-add-view'),
    path('<int:pk>/billing/', CardBillingUpdateView.as_view(), name='card-billing-update'),
    path('', CardListView.as_view(), name='card-list-view'),
]
