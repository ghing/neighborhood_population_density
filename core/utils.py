import logging

from core.models import Geounit, CensusBlock, Neighborhood, Subject, Statistic

def flush_statistics(subject, geounit_cls):
    """Delete all statistics for a certain class of geounits and subject"""
    for geounit in geounit_cls.objects.all():
        try:
            stat = Statistic.objects.get(subject=subject, geounit__id=geounit.id)
            stat.delete()
        except Statistic.DoesNotExist:
            continue

def flush_neighborhood_total_population():
    s = Subject.objects.get(name='Total Population')
    flush_statistics(s, Neighborhood)

def aggregate_subject(subject, geounit_set1, geounit_set2):
    """Aggregate the values of a subject for a geounit of one type with all the geounits of another type that it contains"""

    logger = logging.getLogger('neighborhood_population_density.custom')
    total_processed = 0
    parent_found = 0
    parent_not_found = 0

    for geounit in geounit_set1:
        total_processed += 1
        try:
            parent = geounit_set2.get(geom__contains=geounit.geom.centroid)
        except DoesNotExist:
            parent_not_found += 1
            logging.warn('Parent %s geounit not found for %s geounit %s' %
                (parent.__class__.__name__, geounit.__class__.__name__, geounit))
            continue

        parent_found += 1
        stat = geounit.statistic_set.get(subject=subject)
        parent_stat, created = parent.statistic_set.get_or_create(subject=subject,
            defaults={'value': 0, 'geounit': parent})
        parent_stat.value += stat.value
        parent_stat.save()

    logging.debug("Processed: %d, Parent found: %d, Parent not found: %d" %
        (total_processed, parent_found, parent_not_found))

def aggregate_neighborhood_total_population():
    s = Subject.objects.get(name='Total Population')
    aggregate_subject(s, CensusBlock.objects.all(), Neighborhood.objects.all())

def aggregate_san_francisco_neighborhood_total_population():
    s = Subject.objects.get(name='Total Population')
    aggregate_subject(s, CensusBlock.objects.filter(statefp10='06', countyfp10='075'), Neighborhood.objects.filter(city='San Francisco'))

def trim_geounits(geounit_parent_cls, geounit_child_cls):
    """Delete all geounits that aren't covered by another."""
    geounits_to_delete = geounit_child_cls.objects.all()
    for parent_geounit in geounit_parent_cls.objects.all():
        geounits_to_delete = geounits_to_delete.exclude(geom__coveredby=parent_geounit.geom)

    for geounit in geounits_to_delete:
        geounit.delete()

def trim_san_francisco_blocks_to_neighborhood():
    geounits_to_delete = CensusBlock.objects.filter(statefp10='06', countyfp10='075')
    for neighborhood in Neighborhood.objects.filter(city='San Francisco'):
        geounits_to_delete = geounits_to_delete.exclude(geom__coveredby=neighborhood.geom)

    geounits_to_delete.delete()

def trim_neighborhoods_by_name(neighborhood_names):
    """Remove neighborhoods from system unless their name is in the list"""
    neighborhoods_to_delete = Neighborhood.objects.all()
    for neighborhood_name in neighborhood_names:
        neighborhoods_to_delete = neighborhoods_to_delete.exclude(name=neighborhood_name)

    for neighborhood in neighborhoods_to_delete:
        neighborhood.delete()

def trim_neighborhoods_for_test():
    """Remove neighborhoods from the system except for the ones we're using in our test data"""
    trim_neighborhoods_by_name((
        'Logan Square', 
    ))

def update_population_density(geounit_set):
    subject, created = Subject.objects.get_or_create(name='Population Density')
    for geounit in geounit_set:
        total_population = geounit.statistic_set.get(subject__name='Total Population').value
        area = geounit.area_sq_mi()
        stat = Statistic(subject=subject, geounit=geounit, value=total_population / area)
        stat.save()

def update_neighborhood_population_density():
    update_population_density(Neighborhood.objects.all())

def update_san_francisco_neighborhood_population_density():
    update_population_density(Neighborhood.objects.filter(city='San Francisco'))
