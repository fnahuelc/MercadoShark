from django.shortcuts import render, redirect
from .forms import ItemForm
from .models import Item
from api_connection import Meli_manager
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User

# Init meli manager
meli_manager = Meli_manager()


def index(request):
    if request.user.is_anonymous():
        return render(request, 'managerApp/welcomeFirstTime.html')
    else:
        userData = meli_manager.get_information_user(request.user.profile.access_token)
        if userData:
            currentUser = request.user
            try:
                username = userData['nickname']
            except KeyError:
                return meli_manager.login()
            meli_manager.get_active_items_from_ML(username, currentUser)
            meli_manager.refresh_info_items(currentUser)
            items = Item.objects.filter(user=currentUser)
            delays = [.2*n for n in range(len(items))]
            return render(request, 'managerApp/index.html', {
                            'items': zip(items, delays),
                            'delays': delays})
        else:
            return render(request, 'managerApp/welcome.html')


def create_item(request):

    # if the form is vaild, publish item
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        response = meli_manager.publish_item(form,request.user)

        # In case of Successful response answer
        try:
            permlink = response['permalink']
            meli_manager.create_itemObject(response,'this_username',request.user)
            return render(request, 'managerApp/modal.html', {
                'content':'El articulo se ah publicado con exito!',
                'permlink':permlink})

        # in cases of error
        except (ObjectDoesNotExist, KeyError):
            return response_errors(request, response, 'el articulo no se ah podido publicar.')

        # if the form is not valid will be returned
        # (the first time that the function is called there are no post request)
    context = { "form" : form }
    return render(request, 'managerApp/create_item.html', context)


def closed_item(request,item_id):
    return modify_listening(request, item_id, 'closed')


def paused_item(request,item_id):
    return modify_listening(request, item_id, 'paused')


def active_item(request,item_id):
    return modify_listening(request, item_id, 'active')


def delete_item(request,item_id):
    return modify_listening(request, item_id, 'delete')


def modify_listening(request, item_id, action):
    # get the item if is id is valid
    try:
        item = Item.objects.get(pk=item_id)
    except (RuntimeError, TypeError, NameError, ObjectDoesNotExist) as error:
        return manage_error(request,'El articulo dejo de existir')

    # change the listening item from Mercado Libre
    response = meli_manager.changing_listing_status(item,action,request.user)

        # in case that the answer is error
    if 'error' in response:
        return response_errors(request,response,'La operacion '  + str(action) +', no se ah podido completar. Se obtuvo: ')

    # if is not error will be deleted
    else:
        return index(request)


def authorize_meli(request):
    access_token = meli_manager.authorize_user(request)
    if request.user.is_anonymous():
        return register(request)
    request.user.profile.access_token = access_token
    request.user.save()
    return index(request)


def login_user(request):
    if request.user.is_anonymous():
        return meli_manager.login()
    else:
        username = request.user.username
        return render(request, 'managerApp/welcome.html', {'user': username})


def logout_user(request):
    logout(request)
    return redirect('https://www.mercadolibre.com/jms/mla/lgz/logout/')


def register(request):
    userData = meli_manager.get_information_user(meli_manager.access_token)
    user = authenticate(username=userData['nickname'])
    if user:
        login(request, user)
        return index(request)
    user = User()
    user.username = userData['nickname']
    user.save()
    user.profile.userId = userData['id']
    user.profile.access_token= meli_manager.access_token
    user.save()
    user = authenticate(username=userData['nickname'])
    login(request, user)
    username = user.username
    return render(request, 'managerApp/welcome.html', {'user': username})


def response_errors(request, response, type_error):
    if response['error'] == 'access_token' or response['message'] == 'Malformed access_token: null':
        return login()
    else:
        return render(request, 'managerApp/modal.html', {
            'content': 'Lamentablemente, ' + type_error + ' Se obtuvo: ' + str(
                response['message'])})


def manage_error(request, error):
    return render(request, 'managerApp/modal.html', {
        'content': 'Lamentablemente, hubo un error. Se obtuvo: ' + str(
            error)})