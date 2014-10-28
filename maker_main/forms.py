#coding=utf-8
from django import forms


class GetAPIDataForm(forms.Form):
    request_data = forms.CharField(max_length=1000, required=False)
    sample_url = forms.CharField(max_length=100)
    method = forms.CharField(max_length=10)


class ApiObjectForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500, required=False)
    url_pattern = forms.CharField(max_length=100)
    sample_url = forms.CharField(max_length=100)
    method = forms.CharField(max_length=10)
    request_data = forms.CharField(max_length=100000, required=False)
    response_data = forms.CharField(max_length=100000, required=False)


class EditApiObjectForm(forms.Form):
    category = forms.IntegerField()
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500, required=False)
    url_pattern = forms.CharField(max_length=100)
    sample_url = forms.CharField(max_length=100)
    method = forms.CharField(max_length=10)
    request_data = forms.CharField(max_length=100000, required=False)
    response_data = forms.CharField(max_length=100000, required=False)