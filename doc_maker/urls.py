from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'doc_maker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r"^login/$", "maker_main.views.login"),

    url(r"^$", "maker_main.views.index"),

    url(r"^request_api/$", "maker_main.views.get_api_data"),

    url(r"^api/(?P<api_id>\d+)/$", "maker_main.views.api_page"),

    url(r"^api/(?P<api_id>\d+)/edit/$", "maker_main.views.edit_api"),

    url(r"^api/(?P<api_id>\d+)/delete/$", "maker_main.views.delete_api_page"),

    url(r"^tree_data/$", "maker_main.views.tree_data"),

    url(r"^category/(?P<category_id>\d+)/$", "maker_main.views.category_page"),

    url(r"^category/(?P<category_id>\d+)/add_api/$", "maker_main.views.create_api"),

    url(r"^category/(?P<category_id>\d+)/add_category/$", "maker_main.views.create_category"),

    url(r"^category/(?P<category_id>\d+)/advanced/$", "maker_main.views.category_advanced"),

    url(r"^category/(?P<category_id>\d+)/edit/$", "maker_main.views.edit_category"),
)
