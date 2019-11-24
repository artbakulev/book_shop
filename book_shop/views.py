from django.shortcuts import render, HttpResponse, redirect

from book_shop import common
from book_shop.models import Book, Author
from django.contrib.auth import authenticate, login


def index(req):
    if req.method == "GET":
        return render(req, 'book_shop/index.html')
    if req.method == "POST":
        email, password = req.POST.get('email'), req.POST.get('password')
        user = authenticate(req, username=email, password=password)
        if user is not None:
            login(req, user)
            return redirect('workers_shop')
        else:
            return render(req, 'book_shop/index.html', {"error": "Некорректный логин и/или пароль"})
    return HttpResponse(status=405)


def workers_shop(req):
    if req.method == "GET":
        return render(req, 'book_shop/workers_shop.html')


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
