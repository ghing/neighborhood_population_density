from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'neighborhood_population_density.views.home', name='home'),
    # url(r'^neighborhood_population_density/', include('neighborhood_population_density.foo.urls')),

    url(r'^$', 'neighborhood_population_density.core.views.index', name='index'),
    url(r'^cities/(?P<city_slug>[a-z,\-]+)/$', 'core.views.city_summary'),
    url(r'^cities/(?P<city_slug>[a-z,\-]+)/neighborhoods.json', 'core.views.neighborhoods_json'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url('^qunit/', include('django_qunit.urls')),
)
