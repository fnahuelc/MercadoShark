from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userId = models.CharField(max_length=100)
    test_account = models.BooleanField(default=False)
    access_token = models.CharField(max_length=200, default='No acces token')
    def __str__(self):
        return 'userID: ' + str(self.user)+ ', user:' + str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Item(models.Model):
    user = models.ForeignKey(User, default=1)
    seller = models.CharField(max_length=60, default='No especificado')
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
    status = models.URLField(max_length=50,default='active')


    def __str__(self):
        return self.title + '. Cantidad: ' + str(self.available_quantity) + '. Precio: $' + str(self.price) + ', id ' + str(self.id)


