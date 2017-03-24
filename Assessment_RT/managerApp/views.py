from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>Esta es la app</h1>')

