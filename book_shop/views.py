from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(req):
    return render(req, 'book_shop/index.html')
