from django.shortcuts import render, get_object_or_404, redirect
from .forms import ItemForm, UserMlForm
from .models import Item, MlUser
from ml_lib.meli import Meli
import json
import requests


def publish_item(form,access_token):
    # Save the form as a new object,
    # and made a instance of meli with active account
    item = form.save(commit=False)
    account = MlUser.objects.get(active=True)
    meli = Meli(client_id=account.username,
                client_secret=account.password,
                access_token=access_token)

    # build the publication and return answer
    publication = {
            "condition": item.condition,
            "warranty": item.warranty,
            "currency_id": item.currency_id,
            "accepts_mercadopago": True,
            "description": item.description,
            "listing_type_id": item.listing_type_id,
            "title": item.title,
            "available_quantity": item.available_quantity,
            "price": item.price,
            "buying_mode": item.buying_mode,
            "category_id": item.category_id,
            "pictures": [{"source": item.pictures}]}

    return (json.loads(meli.post("/items", publication, {'access_token': meli.access_token}).content))


def unpublish_item(item,account,access_token):
    # set as status close the item
    meli = Meli(client_id=account.username,client_secret=account.password, access_token=access_token)
    body = {"status":"closed"}
    response = meli.put("/items/"+item.itemId, body, {'access_token':meli.access_token})
    return json.loads(response.content)


def get_all_items(request, access_token):
    # This function creates items of the all publication of all accounts
    [get_items_from_ML(request, account.username, account.password, access_token)
    for account in MlUser.objects.all()]


def get_items_from_ML(request,username, password,access_token,site_id='MLA'):
    # this function get all publications of a single account

    meli = Meli(client_id=username,
                client_secret=password,
                access_token=access_token)
    response = meli.get(path="sites/"+site_id+"/search?nickname="+str(username))
    response_dict = json.loads(response.content)
    itemsResponse = response_dict['results']

    for itemResponse in itemsResponse:
        itemsId = [item.itemId for item in Item.objects.all()]
        if not itemResponse['id'] in itemsId:
            create_itemObject(itemResponse)
    return str(itemsResponse)


def create_itemObject(itemData):
    # this function creates a single item object from item data
    item = Item(
        title=itemData['title'],
        price=itemData['price'],
        available_quantity=itemData['available_quantity'],
        description='nada',
        itemId=itemData['id'],
        pictures=itemData['thumbnail'],
        permalink=itemData['permalink']
    )
    item.account = get_object_or_404(MlUser, active=True)
    item.save()