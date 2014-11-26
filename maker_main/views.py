#coding=utf-8
import json
import requests
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from doc_maker.settings import API_BASE_URL
from .forms import GetAPIDataForm, ApiObjectForm, EditApiObjectForm
from .models import APIObject, Category


def request_api_data(url, method, data=None):
    url = API_BASE_URL + url
    headers = {"content-type": "application/json"}
    headers["Authorization"] = "Token e388bd61a99a08caabb5ef0ce2ebc776ace675a9"
    cookies = {"csrftoken": "111111"}
    headers["X_CSRFTOKEN"] = "111111"
    if method == "GET":
        r = requests.get(url, headers=headers, cookies=cookies)
    elif method == "POST":
        r = requests.post(url, data=data, headers=headers, cookies=cookies)
        print r.request.headers
    elif method == "PUT":
        r = requests.put(url, data=data, headers=headers, cookies=cookies)
    #DELETE
    else:
        r = requests.delete(url, headers=headers, cookies=cookies)
    try:
        return {"status": "success", "response_status_code": r.status_code, "data": r.content}
    except ValueError:
        return {"status": "error", "response_status_code": r.status_code, "content": "Failed to get data"}


def get_api_data(request):
    if request.method == "POST":
        form = GetAPIDataForm(request.POST)
        if form.is_valid():
            r = request_api_data(form.cleaned_data["sample_url"],
                                 form.cleaned_data["method"],
                                 form.cleaned_data["request_data"].encode("utf8"))
            return HttpResponse(json.dumps(r))
        else:
            return HttpResponse(json.dumps({"status": "error", "content": "Invalid form"}), status=400)
    else:
        return HttpResponse(json.dumps({"status": "error"}))


def create_api(request, category_id):
    if request.method == "GET":
        return render(request, "create_api_object.html", {"category_id": category_id})
    else:
        form = ApiObjectForm(request.POST)

        if form.is_valid():
            if form.cleaned_data["response_data"]:
                form.cleaned_data["response_data"] = json.loads(form.cleaned_data["response_data"])
            else:
                form.cleaned_data["response_data"] = None
            if form.cleaned_data["request_data"]:
                form.cleaned_data["request_data"] = json.loads(form.cleaned_data["request_data"])
            else:
                form.cleaned_data["request_data"] = None
            try:
                category = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                raise Http404
            form.cleaned_data["category"] = category
            APIObject.objects.create(**form.cleaned_data)
            return HttpResponse(json.dumps({"status": "success",
                                            "redirect": "/category/" + str(category.id) + "/"}))
        else:
            print form.errors
            return HttpResponse(json.dumps({"status": "error", "content": "Invalid form"}), status=400)


def api_page(request, api_id):
    try:
        api = APIObject.objects.get(pk=api_id)
    except APIObject.DoesNotExist:
        raise Http404
    request_data = json.dumps(api.request_data)
    response_data = json.dumps(api.response_data)
    return render(request, "api_page.html", {"api": api,
                                             "request_data": request_data,
                                             "response_data": response_data,
                                             "api_id": api_id})


def edit_api(request, api_id):
    try:
        api = APIObject.objects.get(pk=api_id)
    except APIObject.DoesNotExist:
        raise Http404
    category = Category.objects.all()
    if request.method == "GET":
        setattr(api, "raw_request_data", json.dumps(api.request_data))
        setattr(api, "raw_response_data", json.dumps(api.response_data))
        return render(request, "edit_api_page.html", {"api": api,
                                                      "method_list": ["GET", "POST", "PUT", "DELETE"],
                                                      "category": category})
    else:

        form = EditApiObjectForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["response_data"]:
                form.cleaned_data["response_data"] = json.loads(form.cleaned_data["response_data"])
            else:
                form.cleaned_data["response_data"] = None
            if form.cleaned_data["request_data"]:
                form.cleaned_data["request_data"] = json.loads(form.cleaned_data["request_data"])
            else:
                form.cleaned_data["request_data"] = None
            try:
                category = Category.objects.get(pk=form.cleaned_data["category"])
                form.cleaned_data["category"] = category
            except Category.DoesNotExist:
                return HttpResponse(json.dumps({"status": "error", "content": "Invalid form"}), status=400)

            APIObject.objects.filter(pk=api_id).update(**form.cleaned_data)
            return HttpResponse(json.dumps({"status": "success",
                                            "redirect": "/category/" + str(api.category_id) + "/"}))
        else:
            print form.errors
            return HttpResponse(json.dumps({"status": "error", "content": "Invalid form"}), status=400)


def tree_data(request):
    data = []
    c = Category.objects.all()
    for item in c:
        is_open = not APIObject.objects.filter(category=item).exists()
        parent = item.get_parent()
        if parent:
            node_data = {"id": str(item.id),
                         "parent": str(parent.id),
                         "text": item.name,
                         "state": {"opened": is_open},
                         "icon": "glyphicon glyphicon-folder-open"}
        else:
            node_data = {"id": str(item.id),
                         "parent": "#",
                         "text": item.name,
                         "state": {"opened": is_open},
                         "icon": "glyphicon glyphicon-folder-open"}
        node_api_data = APIObject.objects.filter(category=item).values("pk", "title")
        for api_item in node_api_data:
            data.append({"id": "api_" + str(api_item["pk"]),
                         "parent": str(item.id),
                         "text": api_item["title"],
                         "icon": "glyphicon glyphicon-file"})
        data.append(node_data)
    return HttpResponse(json.dumps(data))


def category_page(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    #r如果有api 就在本页上显示所有的api
    api = APIObject.objects.filter(category=category)
    if api:
        for item in api:
            setattr(item, "raw_request_data", json.dumps(item.request_data))
            setattr(item, "raw_response_data", json.dumps(item.response_data))
    return render(request, "api_list.html", {"api": api, "category": category})


def search(request):
    keyword = request.GET.get("keyword", None)
    api = APIObject.objects.filter(title__icontains=keyword)
    for item in api:
        setattr(item, "raw_request_data", json.dumps(item.request_data))
        setattr(item, "raw_response_data", json.dumps(item.response_data))
    return render(request, "api_list.html", {"api": api})
    

def create_category(request, category_id):
    try:
        parent_category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    category_name = request.POST.get("category_name", None)
    if not category_name:
        raise Http404
    parent_category.add_child(name=category_name, content=request.POST.get("category_content", None))
    return HttpResponseRedirect("/category/" + str(category_id) + "/")


def category_advanced(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    all_category = Category.objects.all()
    return render(request, "category_advanced.html", {"category": category, "all_category": all_category})


def edit_category(request, category_id):
    parent_category = request.POST.get("parent_category", None)
    name = request.POST.get("category_name", None)
    if not (parent_category and name):
        raise Http404
    try:
        parent_category = Category.objects.get(pk=parent_category)
    except Category.DoesNotExist:
        raise Http404
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    category.name = name
    category.content = request.POST.get("category_content", None)
    category.save()
    category.move(parent_category, "last-child")
    return HttpResponseRedirect("/category/" + str(parent_category.id) + "/")


def delete_api_page(request, api_id):
    APIObject.objects.filter(pk=api_id).delete()
    return HttpResponseRedirect("/category/1/")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponse(json.dumps({"status": "success", "redirect": "/"}))
        return HttpResponse(json.dumps({"status": "error"}))


def create_data():
    root = Category.add_root(name='根目录')


def index(request):
    return HttpResponseRedirect("/category/1/")
