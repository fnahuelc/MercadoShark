from django.shortcuts import render, get_object_or_404, redirect
from .forms import ItemForm, UserMlForm
from .models import Item, MlUser, Globals
from ml_lib.meli import Meli
import json
import requests
from . import itemsControlers


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
            response = itemsControlers.publish_item(form,Globals.objects.all()[0].access_token)

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
    response = itemsControlers.unpublish_item(item,account,Globals.objects.all()[0].access_token)

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


def get_access_token(request, code=None):
    # Get the code from Mercado Libre (after redirect)
    code = request.GET.get('code')

    # if exist the code
    if code:
        # Make the request of the acces token by posting the code
        response = requests.post("https://api.mercadolibre.com/oauth/token?grant_type=authorization_code&client_id=4704790082736526&client_secret=V94M94z1GYoQC5PLXHL95O6mS6p6mOVH&code="+code+"&redirect_uri=http://www.localhost:8000/managerApp/get_access_token/")

        # get the access_token from the answer and save it
        access_token = json.loads(response.content)['access_token']
        current_global = Globals.objects.all()[0]
        current_global.access_token = access_token
        current_global.save()

        # Let know the user about the new acces_token
        return render(request, 'managerApp/modal.html', {'content':'Un nuevo ACCESS TOKEN ah sido creado. Ahora puede comenzar a operar.'})
    return redirect('https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id=4704790082736526')


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
    meli = Meli(account.username, account.password, globals.access_token)
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
