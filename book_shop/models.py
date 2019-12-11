from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Supply(models.Model):
    start = models.DateField(verbose_name="date of supply starting", null=True, blank=True)
    finish = models.DateField(verbose_name="date of supply finishing", null=True, blank=True)

    def __str__(self):
        return f'supply: {self.start} - {self.finish}'


class Book(models.Model):
    title = models.CharField(max_length=100, default="")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, default=None)
    year = models.IntegerField(default=2000)
    price = models.FloatField(default=0.0)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, default=None, null=True)
    TYPES_OF_AVAILABILITY = (
        ('SHOP', 'Available in shop'),
        ('WARE', 'Available in warehouse'),
        ('REQ', 'Available by request'),
    )
    availability = models.CharField(max_length=4, choices=TYPES_OF_AVAILABILITY, default="REQ")
    number_shop = models.IntegerField(default=0)
    number_ware = models.IntegerField(default=0)
    number_init = models.IntegerField(default=0)

    def __str__(self):
        return f'book: {self.title}'


class Request(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    date = models.DateField(verbose_name="date of request", auto_now=True)


class SupplyRequest(Request):
    status = models.BooleanField(verbose_name="status of supply request", default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.client} order supply of {self.book.title}'


class DeliveryRequest(Request):
    status = models.BooleanField(verbose_name="status of delivery request", default=False)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    number = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.worker} order delivery of {self.book.title}'


class Purchase(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    number = models.IntegerField(default=0)
    date = models.DateField(verbose_name="date of purchase", auto_now=True)

    def __str__(self):
        return f'Purchase {self.worker.first_name} of {self.book.title} ({self.date})'
