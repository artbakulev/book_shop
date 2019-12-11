from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect

from book_shop import common
from book_shop.models import Book, Author, DeliveryRequest, Client, Supply, Purchase, SupplyRequest
from django.contrib.auth import authenticate, login, logout as auth_logout
import json
from datetime import datetime


def index(req):
    if req.method == "GET":
        if req.user.is_authenticated:
            return redirect('purchase')
        return render(req, 'book_shop/index.html')
    if req.method == "POST":
        email, password = req.POST.get('email'), req.POST.get('password')
        user = authenticate(req, username=email, password=password)
        if user is not None:
            login(req, user)
            return redirect('purchase')
        else:
            return render(req, 'book_shop/index.html', {"error": "Некорректный логин и/или пароль"})
    return HttpResponse(status=405)


@login_required(login_url='/')
def worker_warehouse_view(req):
    if req.method == "GET":
        requests = DeliveryRequest.objects.all()
        requests = sorted(requests, key=lambda x: x.status)
        books = Book.objects.all()
        return render(req, 'book_shop/warehouse.html', {"requests_nav": 'warehouse', "requests": requests,
                                                        'books': books})


def client_view(req):
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


def book_view(req, book_id):
    if req.method != 'GET':
        return HttpResponse(status=405)
    book_model = Book.objects.get(id=book_id)
    context = {'book': book_model}
    return render(req, 'book_shop/book.html', context)


def author_view(req, author_id):
    if req.method != 'GET':
        return HttpResponse(status=405)
    books_author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=books_author)
    context = {'books': books, 'author': books_author}
    return render(req, 'book_shop/author.html', context)


@login_required(login_url='/')
def logout(req):
    if not req.user.is_authenticated:
        return redirect('index')
    auth_logout(req)
    return redirect('index')


@login_required(login_url='/')
def api_delivery_request(req):
    if not req.user.is_authenticated:
        return HttpResponse(status=401)
    data = json.loads(req.body)
    delivery_request_id = data.get('request_id', False)
    book_id = data.get('book_id', False)
    if not delivery_request_id and not book_id:
        return HttpResponse(status=400)

    if delivery_request_id:
        delivery_request = DeliveryRequest.objects.get(id=delivery_request_id)
        delivery_request.status = True
        delivery_request.save()
        book = delivery_request.book
        book.number_ware -= delivery_request.number
        book.number_shop += delivery_request.number
        book.availability = 'SHOP'
        book.save(update_fields=['number_shop', 'number_ware', 'availability'])
        return HttpResponse(status=200)

    amount = int(data.get('amount', 1))
    try:
        delivery_request = DeliveryRequest.objects.get(book_id=book_id, status=False)
        delivery_request.number += amount
    except DeliveryRequest.DoesNotExist:
        delivery_request = DeliveryRequest.objects.create(worker=req.user, book_id=book_id, number=amount)
    delivery_request.save()
    return HttpResponse(status=200)


@login_required(login_url='/')
def api_supply_requests(req):
    data = json.loads(req.body)
    try:
        client = Client.objects.get(email=data['email'])
    except Client.DoesNotExist:
        client = Client.objects.create(email=data['email'], name=data['name'], phone=data['phone'])
        client.save()
    book = Book.objects.get(id=data['book_id'])
    request = SupplyRequest.objects.create(book=book, client=client)
    request.save()
    return HttpResponse(status=200)


@login_required(login_url='/')
def worker_sell_view(request):
    books = Book.objects.filter(availability='SHOP')
    context = {'books': books, 'requests_nav': 'purchase'}
    if request.method == "POST":
        amount = int(request.POST['sell_amount'])

        book_id = int(request.POST['sell_book_id'])
        book = Book.objects.get(id=book_id)
        if book.number_shop < amount:
            context.update({'message': 'Слишком мало книг в магазине. Сначала закажите книги со склада.'})
            return render(request, 'book_shop/purchase.html', context)

        purchase = Purchase.objects.create(book=book, worker=request.user, number=amount)
        purchase.save()
        book.number_shop -= amount
        if book.number_shop == 0 and book.number_ware > 0:
            book.availability = 'WARE'
        elif book.number_shop == 0 and book.number_ware == 0:
            book.availability = 'REQ'
        book.save(update_fields=['number_shop', 'availability'])

        return render(request, 'book_shop/purchase.html', context)
    return render(request, 'book_shop/purchase.html', context)


@login_required(login_url='/')
def worker_books_view(request):
    books = Book.objects.all()
    return render(request, 'book_shop/books.html', {'books': books, 'requests_nav': 'books'})


@login_required(login_url='/')
def worker_supplies_view(request):
    supplies = Supply.objects.order_by('finish', '-start', '-id')
    books = Book.objects.all()
    context = {"supplies": supplies, 'books': books}
    if request.method == 'POST':
        supply_id = request.POST['supply_id']
        supply = Supply.objects.get(id=supply_id)
        supply.finish = datetime.now()
        supply.save()
        for book in supply.book_set.all():
            book.number_ware += book.number_init
            book.number_init = 0
            book.save(update_fields=['number_init', 'number_ware'])
        return render(request, 'book_shop/supplies.html', context)

    return render(request, 'book_shop/supplies.html', context)


@login_required(login_url='/')
def worker_clients_view(request):
    clients = Client.objects.all()
    books = Book.objects.all()
    return render(request, 'book_shop/clients.html', {'books': books, 'clients': clients, 'requests_nav': 'clients'})
