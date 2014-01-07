from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Amazon_WebService.views.home', name='home'),
    # url(r'^Amazon_WebService/', include('Amazon_WebService.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
)

urlpatterns += patterns('commodity',
    url(r'^api/commodity/$', 'views.get_all_categories'),
    url(r'^api/commodity/field/$', 'views.get_ava_filed'),
    url(r'^api/commodity/custom/$', 'views.custom_query'),
    url(r'^api/commodity/(?P<asin>[A-Z\d]+)/$', 'views.get_single_commodity'),
)
