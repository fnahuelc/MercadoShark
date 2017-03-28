from django.contrib import admin
from .models import Article, MlUser, Globals

admin.site.register(Article)
admin.site.register(MlUser)
admin.site.register(Globals)

