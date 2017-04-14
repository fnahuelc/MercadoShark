from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Globals(models.Model):
    access_token = models.CharField(
        max_length=150,
        default='APP_USR-4704790082736526-032620-7c743ad9f87cedac9f7bfeb331e632a6__L_G__-38184225')


class MlUser(models.Model):
    user = models.ForeignKey(User,default=1)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    userId = models.CharField(max_length=100)
    itemList = models.CharField(max_length=9999)
    test_account = models.BooleanField(default=False)

    def __str__(self):
        return 'userID: ' + str(self.user)+ ', username:' + str(self.username) + ', password: ' + str(self.password)


class Item(models.Model):
    user = models.ForeignKey(User, default=1)
    account = models.ForeignKey(MlUser, default=1)
    title = models.CharField(max_length=60)
    category_id = models.CharField(max_length=60)
    price = models.FloatField(default='10')
    currency_id = models.CharField(max_length=60)
    available_quantity = models.IntegerField(default='1')
    buying_mode = models.CharField(max_length=60)
    listing_type_id = models.CharField(max_length=60)
    condition = models.CharField(max_length=60)
    description = models.CharField(max_length=9999)
    video_id = models.CharField(max_length=60)
    warranty = models.CharField(max_length=60)
    pictures = models.URLField(max_length=2000)
    itemId = models.CharField(max_length=60)
    permalink = models.URLField(max_length=2000)

    def __str__(self):
        return self.title + '. Cantidad: ' + str(self.available_quantity) + '. Precio: $' + str(self.price) + ', id ' + str(self.id)


