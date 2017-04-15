from django.shortcuts import render, get_object_or_404, redirect
from .forms import ItemForm
from .models import Item, MlUser
import itemsControlers
from django.core.exceptions import ObjectDoesNotExist


def create_item(request):

    # if the form is vaild, publish item
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        response = itemsControlers.publish_item(form)

        # In case of Successful response answer
        try:
            permlink = response['permalink']
            itemsControlers.create_itemObject(response,'this_username')

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


def modify_listening(request, item_id, action):
    # get the item if is id is valid
    try:
        item = Item.objects.get(pk=item_id)
    except (RuntimeError, TypeError, NameError, ObjectDoesNotExist) as error:
        return manage_error(request,'El articulo dejo de existir')

    # change the listening item from Mercado Libre
    response = itemsControlers.changing_listing_status(item,action)

        # in case that the answer is error
    if 'error' in response:
        return response_errors(request,response,'La operacion '  + str(action) +', no se ah podido completar. Se obtuvo: ')

    # if is not error will be deleted
    else:
        return index(request)


def login(request):
    return itemsControlers.login()


def authorize_meli(request):
    return itemsControlers.authorize_meli(request)


def closed_item(request,item_id):
    return modify_listening(request, item_id, 'closed')


def paused_item(request,item_id):
    return modify_listening(request, item_id, 'paused')


def active_item(request,item_id):
    return modify_listening(request, item_id, 'active')


def delete_item(request,item_id):
    return modify_listening(request, item_id, 'delete')


def index(request):
    # In case that any account is logged in
    if len(MlUser.objects.all())==0:
        return welcome(request)

    # Get the items publications from MercadoLibre and render them
    userData = info_logged_user(request)
    username = userData['nickname']
    currentUser = MlUser.objects.get(username=username)
    itemsControlers.get_active_items_from_ML(username)
    itemsControlers.refresh_info_items(username)
    items = Item.objects.get(account=currentUser)
    delays = [.2*n for n in range(len(items))]
    return render(request, 'managerApp/index.html',
                         {'items': zip(items,delays),
                          'delays': delays})


def logout(request):
    #Delete all objects from database and the Global instance
    MlUser.objects.all().delete()
    return redirect('https://www.mercadolibre.com/jms/mla/lgz/logout/')


def welcome(request):
    # save current the username
    response = info_logged_user(request)
    user_ml = MlUser(
            username=response['nickname'],
            userId=response['id']
        )
    user_ml.save()
    return render(request, 'managerApp/welcome.html',{'user':user_ml.username})


def info_logged_user(request):
    response = itemsControlers.get_information_user()
    if response['status'] not in (403, 400):
        return response
    else:
        return render(request, 'managerApp/welcomeFirstTime.html')


def response_errors(request,response,type_error):
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