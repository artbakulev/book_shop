from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f'client: {self.name}'


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'author: {self.name}'


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'publisher: {self.name}'


class Book(models.Model):
    title = models.CharField(max_length=100, default="")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, default=None)
    year = models.IntegerField(default=2000)
    price = models.FloatField(default=0.0)
    TYPES_OF_AVAILABILITY = (
        ('SHOP', 'Available in shop'),
        ('WARE', 'Available in warehouse'),
        ('REQ', 'Available by request'),
        ("NOT", "Not available")
    )
    availability = models.CharField(max_length=4, choices=TYPES_OF_AVAILABILITY, default="NOT")
    number = models.IntegerField(default=0)

    def __str__(self):
        return f'book: {self.title}'


class Supply(models.Model):
    start = models.DateField(verbose_name="date of supply starting")
    finish = models.DateField(verbose_name="date of supply finishing")

    def __str__(self):
        return f'supply: {self.start} - {self.finish}'


class SupplyBook(Book):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, default=None)


class Request(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    date = models.DateField(verbose_name="date of request", default=None)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


class SupplyRequest(Request):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    status = models.BooleanField(verbose_name="status of supply request", default=False)

    def __str__(self):
        return f'{self.client} order supply of {self.book.title}'


class DeliveryRequest(Request):
    status = models.BooleanField(verbose_name="status of delivery request", default=False)

    def __str__(self):
        return f'{self.worker} order delivery of {self.book.title}'


class Purchase:
    worker = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    price = models.IntegerField(default=0)
    date = models.DateField(verbose_name="date of purchase", default=None)

    def __str__(self):
        return f'Purchase {self.client.name} of {self.book.title} ({self.date})'
