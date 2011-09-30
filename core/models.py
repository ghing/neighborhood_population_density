from decimal import Decimal
import re

from django.contrib.gis.db import models

class Geounit(models.Model):
    pass

class NeighborhoodManager(models.GeoManager):
    def median_population_density(self, city):
        neighborhoods_sorted = sorted(self.filter(city=city), key=lambda neighborhood: neighborhood.population_density(), reverse=True)
        if ((len(neighborhoods_sorted) % 2) == 1):
            return neighborhoods_sorted[(len(neighborhoods_sorted) / 2) + 1].population_density()
        else:
            return (neighborhoods_sorted[len(neighborhoods_sorted) / 2].population_density() + neighborhoods_sorted[(len(neighborhoods_sorted) / 2) + 1].population_density()) / 2

    def min_population_density(self, city):
        neighborhoods_sorted = sorted(self.filter(city=city), key=lambda neighborhood: neighborhood.population_density())
        return neighborhoods_sorted[0].population_density()

    def max_population_density(self, city):
        neighborhoods_sorted = sorted(self.filter(city=city), key=lambda neighborhood: neighborhood.population_density())
        return neighborhoods_sorted[-1].population_density()

    def cities(self):
        cities = []
        for city_dict in self.values('city').distinct():
            cities.append(city_dict['city'])
        return cities

    def city_slug_to_name(self, city_slug):
        return re.sub('-', ' ', city_slug).title()

    def city_neighborhoods(self, city_slug):
        return self.filter(city=self.city_slug_to_name(city_slug))

class Neighborhood(Geounit):
    """Neighborhood boundary"""

    name = models.CharField(max_length=64)
    area = models.IntegerField(null=True)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=43)
    city = models.CharField(max_length=64)
    region_id = models.FloatField()

    geom = models.MultiPolygonField(srid=4326)
    objects = NeighborhoodManager()

    class Meta:
        verbose_name_plural = "Neighborhood Boundaries"

    def __unicode__(self):
        """Return the string representation of the model."""
        return "%s, %s, %s" % (self.name, self.city, self.state)

    def get_statistic_value(self, subject_name):
        return self.statistic_set.get(subject__name=subject_name).value 

    def total_population(self):
        return self.get_statistic_value('Total Population')

    def population_density(self):
        return self.get_statistic_value('Population Density')

    def area_sq_mi(self, srid=102003):
        """Get area of neighborhood in square miles"""
        self.geom.transform(srid)
        return Decimal('%f' % (self.geom.area / 2589988.11))

neighborhood_mapping = {
    'name' : 'NAME',
    'state' : 'STATE',
    'county' : 'COUNTY',
    'city' : 'CITY',
    'region_id' : 'REGIONID',
    'geom' : 'POLYGON' 
}

class CensusBlock(Geounit):
    statefp10 = models.CharField(max_length=2)
    countyfp10 = models.CharField(max_length=3)
    tractce10 = models.CharField(max_length=6)
    blockce10 = models.CharField(max_length=4)
    geoid10 = models.CharField(max_length=15)
    name10 = models.CharField(max_length=10)
    mtfcc10 = models.CharField(max_length=5)
    ur10 = models.CharField(max_length=1)
    uace10 = models.CharField(max_length=5)
    funcstat10 = models.CharField(max_length=1)
    aland10 = models.FloatField()
    awater10 = models.FloatField()
    intptlat10 = models.CharField(max_length=11)
    intptlon10 = models.CharField(max_length=12)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        """Return the string representation of the model."""
        return "%s" % (self.geoid10)

# Auto-generated `LayerMapping` dictionary for CensusBlock model
censusblock_mapping = {
    'statefp10' : 'STATEFP10',
    'countyfp10' : 'COUNTYFP10',
    'tractce10' : 'TRACTCE10',
    'blockce10' : 'BLOCKCE10',
    'geoid10' : 'GEOID10',
    'name10' : 'NAME10',
    'mtfcc10' : 'MTFCC10',
    'ur10' : 'UR10',
    'uace10' : 'UACE10',
    'funcstat10' : 'FUNCSTAT10',
    'aland10' : 'ALAND10',
    'awater10' : 'AWATER10',
    'intptlat10' : 'INTPTLAT10',
    'intptlon10' : 'INTPTLON10',
    'geom' : 'MULTIPOLYGON',
}

class Subject(models.Model):
    """A type of data that pertains to one or more geounits"""
    name = models.CharField(max_length=64)

    def __unicode__(self):
        """Return the string representation of the model."""
        return "%s" % (self.name)

class Statistic(models.Model):
    """An instance of a subject for a particular geounit"""
    subject = models.ForeignKey(Subject)
    geounit = models.ForeignKey(Geounit)
    value =  models.DecimalField(max_digits=12, decimal_places=4)
