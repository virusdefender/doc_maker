#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from treebeard.mp_tree import MP_Node
from jsonfield import JSONField


class Category(MP_Node):
    name = models.CharField(max_length=30)
    content = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name


class APIObject(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    url_pattern = models.CharField(max_length=400)
    sample_url = models.CharField(max_length=400)
    method = models.CharField(max_length=10)
    request_data = JSONField(blank=True, null=True)
    response_data = JSONField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    #author = models.ForeignKey(User)


class APIParameter(models.Model):
    api_object = models.ForeignKey(APIObject)
    parameter = models.CharField(max_length=30)
    value = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    data_type = models.CharField(max_length=10)


class ResponseStatus(models.Model):
    api_object = models.ForeignKey(APIObject)
    status_code = models.IntegerField()
    content = models.TextField()