from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from core.models import Neighborhood, neighborhood_mapping 

class Command(BaseCommand):
    args = '<shapefile shapefile ...>'
    help = 'Imports neighborhood boundaries from a Zillow Shapefile'

    def handle(self, *args, **options):
        for shapefile in args:
            lm = LayerMapping(Neighborhood, shapefile, neighborhood_mapping,
                              transform=True, encoding='iso-8859-1')
            lm.save(strict=True, verbose=True)


