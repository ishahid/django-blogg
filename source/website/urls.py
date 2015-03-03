from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blogg.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
)
