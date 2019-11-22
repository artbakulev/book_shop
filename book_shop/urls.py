from django.urls import path
import book_shop.views as views

urlpatterns = [
    path(r'', views.index),
    path(r'client', views.client),
]
