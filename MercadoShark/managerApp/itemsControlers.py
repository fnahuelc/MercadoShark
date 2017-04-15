from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, MlUser
import json
from ml_lib.meli import Meli

# Global meli class
appID =  4704790082736526
secretID = 'V94M94z1GYoQC5PLXHL95O6mS6p6mOVH'
REDIRECT_URI = 'https://fnahuelc.pythonanywhere.com/managerApp/authorize_meli'
meli = Meli(client_id=appID,client_secret=secretID)


def publish_item(form):
    # Save the form as a new object,
    # and made a instance of meli with active account
    item = form.save(commit=False)

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


def changing_listing_status(item,status):
    # set as status close the item
    if status == 'delete':
        body = {"deleted": "true"}
        response = meli.put("/items/" + item.itemId, body, {'access_token': meli.access_token})
        item.delete()
    else:
        body = {"status": status}
        response = meli.put("/items/" + item.itemId, body, {'access_token': meli.access_token})
    return json.loads(response.content)


def get_information_user():
    response = meli.get(path="users/me?access_token="+str(meli.access_token))
    response_dict = json.loads(response.content)
    return response_dict

def get_active_items_from_ML(username,site_id='MLA'):
    # this function get all publications of a single account
    response = meli.get(path="sites/"+site_id+"/search?nickname="+str(username))
    response_dict = json.loads(response.content)
    itemsResponse = response_dict['results']

    for itemResponse in itemsResponse:
        itemsId = [item.itemId for item in Item.objects.all()]
        if not itemResponse['id'] in itemsId:
            create_itemObject(itemResponse,username)


def refresh_info_items():
    for item in Item.objects.all():
        response = meli.get(path="items/"+item.itemId)
        data = json.loads(response.content)
        if 'error' in data:
            item.delete()

        item.title = data['title']
        item.price = data['price']
        item.available_quantity = data['available_quantity']
        item.description = data['descriptions']
        item.pictures = data['thumbnail']
        item.permalink = data['permalink']
        item.status = data['status']
        item.save()


def create_itemObject(itemData,username):
    # this function creates a single item object from item data
    userData = get_information_user()
    username = userData['nickname']
    currentUser = MlUser.objects.get(username=username)

    if username == 'this_username':
        username = currentUser.username
    item = Item(
        title=itemData['title'],
        seller = username,
        price=itemData['price'],
        available_quantity=itemData['available_quantity'],
        description='nada',
        itemId=itemData['id'],
        pictures=itemData['thumbnail'],
        permalink=itemData['permalink'],

    )
    item.save()


def login():
    redirectURI = redirect(meli.auth_url(redirect_URI=REDIRECT_URI))
    return redirectURI


def authorize_meli(request):
    code = request.GET.get('code')
    if code:
        meli.authorize(code, REDIRECT_URI)
        print ('se creo un nuevo access token', meli.access_token)
        return render(request, 'managerApp/modal.html', {
            'content': 'Se ah creado un nuevo acces token. Puede continuar operando'})

    return authorize_meli(request)
