from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleForm, UserMlForm
from .models import Article, MlUser, Globals
from ml_lib.meli import Meli
import json
import requests

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
globals = Globals()
globals.save()

def create_article(request):
    if not MlUser.objects.get(active=True):
        return render(request, 'managerApp/login_mlUser.html')
    else:
        form = ArticleForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.account = get_object_or_404(MlUser, active=True)

            meli = Meli(client_id='38184225', client_secret='30120422', access_token=globals.access_token)
            body = {"condition": article.condition,
                    "warranty": article.warranty,
                    "currency_id": article.currency_id,
                    "accepts_mercadopago": True,
                    "description": article.description,
                    "listing_type_id": article.listing_type_id,
                    "title": article.title,
                    "available_quantity": article.available_quantity,
                    "price": article.price,
                    "buying_mode": article.buying_mode,
                    "category_id": article.category_id,
                    "pictures": [{"source": article.pictures}]}

            response = meli.post("/items", body, {'access_token': meli.access_token})
            article.save()
            return render(request, 'managerApp/modal.html', {'content':'El articulo se ah publicado con exito!'})

        context = { "form" : form }
        return render(request, 'managerApp/create_article.html', context)


def delete_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except:
        return index(request)
    try:
        account = MlUser.objects.get(active=True)
    except:
        MlUser.objects.all()[0].active = True
        account = MlUser.objects.get(active=True)

    meli = Meli(client_id=account.username,client_secret=account.password, access_token=globals.access_token)
    body = {"status":"closed"}
    response = meli.put("/items/"+article.itemId, body, {'access_token':meli.access_token})
    respuesta = json.loads(response.content)
    try:
        respuesta['error']
        return get_access_token(request)
    except:
        article.delete()
        return index(request)


def get_all_items(request):
    #Article.objects.all().delete()
    [get_articles_from_ML(request, account.username, account.password)
    for account in MlUser.objects.all()]


def set_current_account(request):
    try:
        account = MlUser.objects.get(active=True)
    except:
        try:
            account = MlUser.objects.all()[0]
        except:
            login_mlUser(request)
    meli = Meli(client_id=account.username,client_secret=account.password, access_token=globals.access_token)
    response = json.loads(meli.get("/users/me?access_token="+str(globals.access_token)).content)
    try:
        if response['message'] == 'invalid_token':
            return get_access_token(request)
        return show_response(request,'respuesta',response)
    except:
        pass
    globals.current_account = response['nickname']
    globals.save()
    return


def delete_account(request, account_id):
    try:
        mlUser = MlUser.objects.get(pk=account_id)
        mlUser.delete()
    except:
        pass
    accounts = MlUser.objects.all()
    try:
        accounts[0].active = True
        accounts[0].save()
        account_active = MlUser.objects.get(active=True)
    except:
        account_active = None

    articles = Article.objects.all()
    accounts = MlUser.objects.all()

    return index(request)


def index(request):
    if len(MlUser.objects.all())==0:
        return render(request, 'managerApp/login_mlUser.html')

    set_current_account(request)
    get_all_items(request)
    accounts = MlUser.objects.all()
    articles = Article.objects.all()
    delays = [.2*n for n in range(len(articles))]
    return render(request, 'managerApp/index.html',
                         {'articles': zip(articles,delays),
                          'accounts': accounts,
                          'current_account': globals.current_account,
                          'delays': delays})


def select_account(request, account_id):
    try:
        ml_account_old = MlUser.objects.get(active=True)
        ml_account_old.active = False;
        ml_account_old.save()

    except:
        pass
    ml_account = MlUser.objects.get(id=account_id)
    ml_account.active = True;
    ml_account.save()

    accounts = MlUser.objects.all()
    articles = Article.objects.filter(account=ml_account)

    return render(request, 'managerApp/index.html', {'articles': articles, 'accounts':accounts, 'current_account':globals.current_account})


def get_access_token(request, code=None, aditional_info=None):
    code = request.GET.get('code')
    if code:
        response = requests.post("https://api.mercadolibre.com/oauth/token?grant_type=authorization_code&client_id=4704790082736526&client_secret=V94M94z1GYoQC5PLXHL95O6mS6p6mOVH&code="+code+"&redirect_uri=http://www.localhost:8000/managerApp/get_access_token/")
        access_token = json.loads(response.content)['access_token']
        globals.access_token = access_token
        globals.save()
        if aditional_info:
            return render(request, 'managerApp/modal.html', {'content':'Un nuevo ACCESS TOKEN ah sido creado ,'+str(aditional_info)})
        else:
            return render(request, 'managerApp/modal.html', {'content':'Un nuevo ACCESS TOKEN ah sido creado. Ahora puede comenzar a operar.'})
    return redirect('https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id=4704790082736526')


def create_testUser(request):
    account = MlUser.objects.get(active=True)
    meli = Meli(account.username,account.password,globals.access_token)
    body = {"site_id":"MLA"}
    response = meli.post("/users/test_user", body, {'access_token': globals.access_token})

    return show_response(request, 'El resultado de crear un nuevo test user es ', str(response.content))


def login_mlUser(request):
    form = UserMlForm(request.POST or None)
    if form.is_valid():
        try:
            ml_account_old = MlUser.objects.get(active=True)
            ml_account_old.active = False;
            ml_account_old.save()
        except:
            pass
        user_ml = form.save(commit=False)
        user_ml.access_token = globals.access_token

        client_id = str(user_ml.username)
        client_secret = str(user_ml.password)

        user_ml.save()
        get_articles_from_ML(request, client_id,client_secret)
        return get_access_token(request,None,' para poder completar su solicitud. Por favor, intente nuevamente')
    context = {"form": form}
    return render(request,'managerApp/login_mlUser.html', context)


def get_articles_from_ML(request,username, password,site_id='MLA'):
    meli = Meli(client_id=username,
                client_secret=password,
                access_token=globals.access_token)
    response = meli.get(path="sites/"+site_id+"/search?nickname="+str(username))
    response_dict = json.loads(response.content)
    items = response_dict['results']
    articlesId = [article.itemId for article in Article.objects.all()]
    for item in items:
        if not item['id'] in articlesId:
            article = Article(

                title=item['title'],
                price=item['price'],
                available_quantity=item['available_quantity'],
                description='nada',
                itemId = item['id'],
                pictures=item['thumbnail'],
                permalink=item['permalink']
            )
            article.account = get_object_or_404(MlUser, active=True)
            article.save()
    return str(items)

def publicate_items_in_ML(request,username, password,site_id='MLA'):
    meli = Meli(client_id=username,
                client_secret=password,
                access_token=globals.access_token)

    params = {'access_token': meli.access_token}
    body = {'title': "Anteojos Ray Ban Wayfare", 'category_id': "MLA5529", 'price': 10, 'currency_id': "ARS",
            'available_quantity': 1, 'buying_mode': "buy_it_now", 'listing_type_id': "bronze", 'condition': "new",
            'description': "Item:,  Ray-Ban WAYFARER Gloss Black RB2140 901  Model: RB2140. Size: 50mm. Name: WAYFARER. Color: Gloss Black. Includes Ray-Ban Carrying Case and Cleaning Cloth. New in Box",
            'video_id': "YOUTUBE_ID_HERE", 'warranty': "12 months by Ray Ban", 'pictures': [
            {'source': "https://upload.wikimedia.org/wikipedia/commons/f/fd/Ray_Ban_Original_Wayfarer.jpg"},
            {'source': "https://en.wikipedia.org/wiki/File:Teashades.gif"}]}
    response1 = meli.post(path="/items", body=body, params=params)
    response = get_articles_from_ML(request,username, password,site_id='MLA')
    return str(response1.content)

def show_response(request,title, response):
    return render(request, 'managerApp/show_response.html', {'response': response, 'title':title})

