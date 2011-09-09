from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from core.models import CensusBlock, censusblock_mapping 

class Command(BaseCommand):
    args = '<shapefile shapefile ...>'
    help = 'Imports census block boundaries from a TIGER Shapefile'

    def handle(self, *args, **options):
        for shapefile in args:
            print shapefile
            lm = LayerMapping(CensusBlock, shapefile, censusblock_mapping,
                              transform=True, encoding='iso-8859-1')
            lm.save(strict=True, verbose=True)


