from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    user = models.ForeignKey(User, default=1)
    title = models.CharField(max_length=60)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.CharField(max_length=9999)
    image = models.URLField(default='https://http2.mlstatic.com/notebook-asus-f555ua-eh71-core-i7-6gen-1tb-8gb-156-pulgadas-D_NQ_NP_971115-MLA25208512372_122016-O.webp')

    def __str__(self):
        return self.title + '. Cantidad: ' + str(self.quantity) + '. Precio: $' + str(self.price) + ', id ' + str(self.id)


