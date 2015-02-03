from django.conf.urls import patterns, include, url
from django.contrib import admin
from Table.views import *

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', index),
    url(r'^index/', index),
    url(r'^data/', get_data),
)
