from django.shortcuts import render, HttpResponse, redirect

from book_shop import common
from book_shop.models import Book, Author, DeliveryRequest, SupplyRequest
from django.contrib.auth import authenticate, login, logout as auth_logout
import json


def index(req):
    if req.method == "GET":
        if req.user.is_authenticated:
            return redirect('worker_main')
        return render(req, 'book_shop/index.html')
    if req.method == "POST":
        email, password = req.POST.get('email'), req.POST.get('password')
        user = authenticate(req, username=email, password=password)
        if user is not None:
            login(req, user)
            return redirect('worker_main')
        else:
            return render(req, 'book_shop/index.html', {"error": "Некорректный логин и/или пароль"})
    return HttpResponse(status=405)


def worker_main(req):
    if req.method == "GET":
        requests = DeliveryRequest.objects.all()
        requests = sorted(requests, key=lambda x: x.status)

        return render(req, 'book_shop/worker-main.html', {"requests_nav": True, "requests": requests})


def client(req):
    if req.method != 'GET':
        return HttpResponse(status=405)
    search_query = req.GET.get('searchQuery', False)
    context = {'inputValue': "", "searchInfo": False, "authors": False}
    if not search_query:
        context.update({"first_time": True})
        return render(req, 'book_shop/client.html', context)
    # TODO: sqlite не поддерживает case-match))) баг с первой верхней буквой
    books = Book.objects.filter(title__icontains=search_query)
    context.update(common.get_books_search_info(len(books)))
    context.update({'books': books})
    authors = Author.objects.filter(name__icontains=search_query)
    print(authors)
    if len(authors) > 0:
        context.update({'authors': authors})
    context['inputValue'] = search_query
    return render(req, 'book_shop/client.html', context)


def book(req, book_id):
    if req.method != 'GET':
        return HttpResponse(status=405)
    book_model = Book.objects.get(id=book_id)
    context = {'book': book_model}
    return render(req, 'book_shop/book.html', context)


def author(req, author_id):
    if req.method != 'GET':
        return HttpResponse(status=405)
    books_author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=books_author)
    context = {'books': books, 'author': books_author}
    return render(req, 'book_shop/author.html', context)


def logout(req):
    if not req.user.is_authenticated:
        return redirect('index')
    auth_logout(req)
    return redirect('index')


def api_delivery_request(req):
    if not req.user.is_authenticated:
        return HttpResponse(status=401)
    delivery_request_id = json.loads(req.body).get('request_id', False)
    if not delivery_request_id:
        return HttpResponse(status=400)
    delivery_request = DeliveryRequest.objects.get(id=delivery_request_id)
    delivery_request.status = True
    delivery_request.save()
    return HttpResponse(status=200)
