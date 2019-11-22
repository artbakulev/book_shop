from django.shortcuts import render, HttpResponse

from book_shop import common
from book_shop.models import Book, Author


def index(req):
    return render(req, 'book_shop/index.html')


def client(req):
    if req.method != 'GET':
        return HttpResponse(405, "Method not allowed")
    search_query = req.GET.get('searchQuery', False)
    context = {'inputValue': "", "searchInfo": False, "authors": False}
    if not search_query:
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
