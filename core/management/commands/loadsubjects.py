import csv
import sys
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from core.models import CensusBlock, Subject, Statistic

class Command(BaseCommand):
    args = '<csvfile>'
    option_list = BaseCommand.option_list + (
        make_option('-s', '--subject',
            action='store',
            dest='subject',
            help='Name of subject to load'),
        make_option('-g', '--geoidfield',
            action='store',
            dest='geoidfield',
            help='Census Block GEOID field in file'),
        make_option('-V', '--valuefield',
            action='store',
            dest='valuefield',
            help='Subject value field in file'),
    )
    help = 'Imports block subject from a CSV file'

    def handle(self, *args, **options):
        subject, created = Subject.objects.get_or_create(name=options['subject'])

        for csvfile in args:
            subject_reader = csv.DictReader(open(csvfile, 'rb'))
            for row in subject_reader:
                try:
                    block = CensusBlock.objects.get(geoid10=row[options['geoidfield']].strip())
                    stat = Statistic(subject=subject, geounit=block, value=row[options['valuefield']])
                    sys.stderr.write("Setting %s for %s to %s\n" %
                        (subject.name, stat.geounit.geoid10, stat.value))
                    stat.save()

                except ObjectDoesNotExist:
                    # Some blocks might not exist in our system since we're
                    # likely only loading ones in the cities.
                    sys.stderr.write("Block with GEOID10 %s not found in system\n" %
                                     (row[options['geoidfield']].strip()))
