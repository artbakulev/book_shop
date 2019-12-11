from django.urls import path
import book_shop.views as views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'client', views.client_view, name='client'),
    path(r'books/<int:book_id>/', views.book_view, name='book'),
    path(r'authors/<int:author_id>/', views.author_view, name='author'),
    path(r'workers/', views.worker_sell_view, name='purchase'),
    path(r'workers/books', views.worker_books_view, name='books'),
    path(r'workers/warehouse', views.worker_warehouse_view, name='warehouse'),
    path(r'workers/supplies', views.worker_supplies_view, name='supplies'),
    path(r'workers/clients', views.worker_clients_view, name='clients'),
    path(r'logout/', views.logout, name='logout'),

    path(r'api/delivery_requests/', views.api_delivery_request, name='api_delivery_request'),
    path(r'api/supply_requests/', views.api_supply_requests, name='api_supply_request'),
]
