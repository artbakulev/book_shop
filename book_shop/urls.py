from django.urls import path
import book_shop.views as views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'client', views.client, name='client'),
    path(r'books/<int:book_id>/', views.book, name='book'),
    path(r'authors/<int:author_id>/', views.author, name='author'),
    path(r'workers/', views.worker_main, name='worker_main'),
    path(r'logout/', views.logout, name='logout'),


    path(r'api/delivery_requests/', views.api_delivery_request, name='api_delivery_request'),
]
