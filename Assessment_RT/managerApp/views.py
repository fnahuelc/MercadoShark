from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ArticleForm, UserForm
from .models import Article

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_article(request):
    if not request.user.is_authenticated():
        return render(request, 'managerApp/login.html')
    else:
        form = ArticleForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            '''
            article.image = request.FILES['image']
            file_type = article.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'article': article,
                    'form': form,
                    'error_message': 'El tipo de imagen debe ser PNG, JPG, or JPEG',
                }
                return render(request, 'managerApp/create_article.html', context)
            '''
            article.save()
            return render(request, 'managerApp/detail.html', {'article': article})
        context = { "form" : form }
        return render(request, 'managerApp/create_article.html', context)


def delete_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.delete()
    articles = Article.objects.filter(user=request.user)
    return render(request, 'managerApp/index.html', {'articles': articles})


def detail(request, article_id):
    if not request.user.is_authenticated():
        return render(request, 'managerApp/login.html')
    else:
        user = request.user
        article = get_object_or_404(Article, pk=article_id)
        return render(request, 'managerApp/detail.html', {'article': article, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'managerApp/login.html')
    else:
        articles = Article.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            articles = articles.filter(
                Q(article_title__icontains=query) |
                Q(article__icontains=query)
            ).distinct()
            return render(request, 'managerApp/index.html', {'articles': articles})
        else:
            return render(request, 'managerApp/index.html', {'articles': articles})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'managerApp/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                articles = Article.objects.filter(user=request.user)
                return render(request, 'managerApp/index.html', {'articles': articles})
            else:
                return render(request, 'managerApp/login.html', {'error_message': 'Su cuenta ah sido desahbilitada'})
        else:
            return render(request, 'managerApp/login.html', {'error_message': 'Invalid login'})
    return render(request, 'managerApp/login.html')

