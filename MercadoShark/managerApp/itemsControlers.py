from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
import json
from ml_lib.meli import Meli
from django.contrib.auth.models import User


class Meli_manager(Meli):
    appID = 4704790082736526
    secretID = 'V94M94z1GYoQC5PLXHL95O6mS6p6mOVH'
    REDIRECT_URI = 'https://fnahuelc.pythonanywhere.com/managerApp/authorize_meli'

    #client_id = 7292933213227627
    #client_secret = 'hElyNu2AWz4btCFGEgYu9997WeopUod0'
    #REDIRECT_URI = 'http://www.localhost:8000/managerApp/authorize_meli'

    def __init__(self):
        super(Meli_manager, self).__init__(client_id=self.client_id, client_secret=self.client_secret)

    def publish_item(self,form, currentUser):
        access_token = currentUser.profile.access_token
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
        return (json.loads(self.post("/items", publication, {'access_token': access_token}).content))


    def changing_listing_status(self,item,status,currentUser):
        # set as status close the item
        access_token = currentUser.profile.access_token
        if status == 'delete':
            body = {"deleted": "true"}
            response = self.put("/items/" + item.itemId, body, {'access_token': access_token})
            item.delete()
        else:
            body = {"status": status}
            response = self.put("/items/" + item.itemId, body, {'access_token': access_token})
        return json.loads(response.content)


    def get_information_user(self,access_token):
        response = self.get(path="users/me?access_token="+str(access_token))
        response_dict = json.loads(response.content)
        if response_dict['status'] not in (403, 400):
            return response_dict
        else:
            return None



    def get_active_items_from_ML(self,username,currentUser,site_id='MLA'):
        # this function get all publications of a single account
        response = self.get(path="sites/"+site_id+"/search?nickname="+str(username))
        response_dict = json.loads(response.content)
        itemsResponse = response_dict['results']

        for itemResponse in itemsResponse:
            itemsId = [item.itemId for item in Item.objects.all()]
            if not itemResponse['id'] in itemsId:
                self.create_itemObject(itemResponse,username,currentUser)


    def refresh_info_items(self,currentUser):
        for item in Item.objects.filter(user=currentUser):
            response = self.get(path="items/"+item.itemId)
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


    def create_itemObject(self,itemData,username,currentUser):
        # this function creates a single item object from item data
        if username == 'this_username':
            username = currentUser.username
        item = Item(
            title=itemData['title'],
            user = currentUser,
            seller = username,
            price=itemData['price'],
            available_quantity=itemData['available_quantity'],
            description='nada',
            itemId=itemData['id'],
            pictures=itemData['thumbnail'],
            permalink=itemData['permalink'],
        )
        item.save()


    def login(self):
        redirectURI = redirect(self.auth_url(redirect_URI=self.REDIRECT_URI))
        return redirectURI


    def authorize_meli(self,request):
        code = request.GET.get('code')
        if code:
            access_token = self.authorize(code, self.REDIRECT_URI)
            print ('se creo un nuevo access token', access_token)
            return access_token
        return self.authorize_meli(request)
