from django.shortcuts import render, get_object_or_404, redirect
from .forms import ItemForm, UserMlForm
from .models import Item, MlUser, Globals
from ml_lib.meli import Meli
import json
import requests
from . import itemsControlers
import sys


def init_globals():
    # made an instance of globals (access_token) and delete the past ones
    # this is called in the the index if is not logged any account
    Globals.objects.all().delete()
    globals = Globals()
    globals.save()


def create_item(request):
    # in case that there are is not an active account
    if not MlUser.objects.get(active=True):
        return render(request, 'managerApp/login_mlUser.html')

    else:
        # if the form is vaild, publish item
        form = ItemForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            response = itemsControlers.publish_item(form,meli)

            # In case of Successful response answer
            try:
                permlink = response['permalink']
                return render(request, 'managerApp/modal.html', {
                    'content':'El articulo se ah publicado con exito!',
                    'permlink':permlink})

            # in cases of error
            except:
                return render(request, 'managerApp/modal.html', {
                    'content': 'Lamentablemente, el articulo no se ah podido publicar. Se obtuvo: ' + str(response['message'])})

        # if the form is not valid will be returned
        # (the first time that the function is called there are no post request)
        context = { "form" : form }
        return render(request, 'managerApp/create_item.html', context)


def delete_items(request, item_id):
    # get the item if is id is valid
    try:
        item = Item.objects.get(pk=item_id)
    except:
        return index(request)

    # try to find the active account or set one as active
    try:
        account = MlUser.objects.get(active=True)
    except:
        MlUser.objects.all()[0].active = True
        account = MlUser.objects.get(active=True)

    # unpublish the item from Mercado Libre
    response = itemsControlers.unpublish_item(item,meli)

    # in case that the answer is error
    try:
        error = response['error']
        if error == 'acces_token':
            return get_access_token(request)
        else:
            return render(request, 'managerApp/modal.html', {
                'content': 'Lamentablemente, el articulo no se ah podido eliminar. Se obtuvo: ' + str(
                    response['message'])})

    # if is not error will be deleted
    except:
        item.delete()
        return index(request)


def delete_account(request, account_id):
    # in the case that the selected account is valid will be deleted
    try:
        mlUser = MlUser.objects.get(pk=account_id)
        mlUser.delete()
    except:
        pass

    # Choose other account as active
    accounts = MlUser.objects.all()
    try:
        accounts[0].active = True
        accounts[0].save()
    except:
        pass
    return index(request)


def index(request):
    # In case that any account is logged in

    if len(MlUser.objects.all())==0:
        init_globals()
        return render(request, 'managerApp/login_mlUser.html')

    # Get the items publications from MercadoLibre and render them
    itemsControlers.get_all_items(request,Globals.objects.all()[0].access_token)
    accounts = MlUser.objects.all()
    items = Item.objects.all()
    delays = [.2*n for n in range(len(items))]
    return render(request, 'managerApp/index.html',
                         {'items': zip(items,delays),
                          'accounts': accounts,
                          'delays': delays})


def logout(request):
    #Delete all objects from database and the Global instance
    MlUser.objects.all().delete()
    Globals.objects.all().delete()
    return redirect('https://www.mercadolibre.com/jms/mla/lgz/logout/')


def select_account(request, account_id):
    # Test that exist an active account
    try:
        ml_account_old = MlUser.objects.get(active=True)
        ml_account_old.active = False
        ml_account_old.save()
    except:
        pass

    # Set the ml account as active
    ml_account = MlUser.objects.get(id=account_id)
    ml_account.active = True
    ml_account.save()

    # Filter and show the items of specified account
    accounts = MlUser.objects.all()
    items = Item.objects.filter(account=ml_account)
    delays = [.2*n for n in range(len(items))]

    return render(request, 'managerApp/index.html', {'items': zip(items,delays), 'accounts': accounts})


appID = 4704790082736526
secretID = 'V94M94z1GYoQC5PLXHL95O6mS6p6mOVH'
meli = Meli(client_id=appID,client_secret=secretID)
REDIRECT_URI = 'http://www.localhost:8000/managerApp/authorize_meli'

def get_access_token(request):
    redirectURI = redirect(meli.auth_url(redirect_URI=REDIRECT_URI))
    return redirectURI

def authorize_meli(request):
    code = request.GET.get('code')
    if code:
        meli.authorize(code, REDIRECT_URI)
        print ('se creo un nuevo access token', meli.access_token)
    return index(request)

def create_testUser(request):
    # This is not working at the moment because I already reach the 10 test users.
    # I just have the information of one:
    # "id": 249620029,
    # "nickname": "TETE9430306",
    # "password": "qatest4690",
    # "site_status": "active",
    # "email": "test_user_30720982@testuser.com"

    # Get the active account and made a post request to Mercado Libre
    account = MlUser.objects.get(active=True)
    body = {"site_id": "MLA"}
    response = json.loads(meli.post("/users/test_user",
                                body,
                                {'access_token': globals.access_token}).content)

    # In case of error
    try:
        error = response['error']
        return render(request, 'managerApp/modal.html', {'content': 'Ah habido un problema en la creacion del Test User, la '
                                                             'devolucion fue: ,' + str(response)})
    # In the case of successful
    except:
        return render(request, 'managerApp/modal.html',
                      {'content': 'El test user fue creado correctamente, la informacion es: ' + str(response)})


def login_mlUser(request):
    # if the form is vaild, create a new account

    form = UserMlForm(request.POST or None)
    if form.is_valid():

        # set the current active account in false (no active)
        try:
            ml_account_old = MlUser.objects.get(active=True)
            ml_account_old.active = False;
            ml_account_old.save()
        except:
            pass

        # save the new account
        user_ml = form.save(commit=False)
        user_ml.save()

        # get a new acces token
        return get_access_token(request)

    # if the form is not valid will be returned
    # (the first time that the function is called there are no post request)
    context = {"form": form}
    return render(request,'managerApp/login_mlUser.html', context)

