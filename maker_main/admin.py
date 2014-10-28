#coding=utf-8
from django.contrib import admin
from .models import Category, APIObject, APIParameter, ResponseStatus

admin.site.register(APIObject)
admin.site.register(APIParameter)
admin.site.register(Category)
admin.site.register(ResponseStatus)
