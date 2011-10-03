from django.shortcuts import render_to_response
from django.template import RequestContext
from django import http
from django.utils import simplejson as json

from core.models import Neighborhood

def index(request):
    city_stats = []
    for city in Neighborhood.objects.cities():
        neighborhoods = sorted(Neighborhood.objects.filter(city=city), key=lambda neighborhood: neighborhood.population_density(), reverse=True)
        city_data = {
            'name': city,
            'neighborhoods': neighborhoods,
            'median_population_density': Neighborhood.objects.median_population_density(city=city),
        }
        city_stats.append(city_data)
        

    return render_to_response('index.html', 
        RequestContext(request, {
            'city_stats': city_stats,
        }))

def neighborhoods_json(request, city_slug):
    neighborhood_json = []
    for neighborhood in Neighborhood.objects.city_neighborhoods(city_slug):
        neighborhood_json.append('{ "type": "Feature", "geometry": %s, "properties": { "name": "%s", "population_density": "%s" } }' % (neighborhood.geom.json, neighborhood.name, neighborhood.population_density()))

    content = '{ "type": "FeatureCollection", "features": ['
    content += ','.join(neighborhood_json)
    content += '] }'

    return http.HttpResponse(content,
                             content_type='application/json')

def city_summary(request, city_slug):
    city = Neighborhood.objects.city_slug_to_name(city_slug)
    neighborhoods = sorted(Neighborhood.objects.filter(city=city), key=lambda neighborhood: neighborhood.population_density(), reverse=True)
    city_data = {
        'name': city,
        'slug': city_slug,
        'neighborhoods': neighborhoods,
        'min_population_density': Neighborhood.objects.min_population_density(city=city),
        'max_population_density': Neighborhood.objects.max_population_density(city=city),
        'median_population_density': Neighborhood.objects.median_population_density(city=city),
    }

    return render_to_response('city_summary.html', 
        RequestContext(request, {
            'city': city_data,
        }))

