from django.urls import path
import book_shop.views as views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'client', views.client, name='client'),
    path(r'books/<int:book_id>/', views.book, name='book'),
    path(r'authors/<int:author_id>/', views.author, name='author'),
    path(r'workers/shop/', views.workers_shop, name='workers_shop'),
]
