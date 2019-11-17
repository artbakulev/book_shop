from django.urls import path
import book_shop.views as views

urlpatterns = [
    path('', views.index)
]
