from decimal import Decimal

from django.test import TestCase

from core.models import Neighborhood, CensusBlock, Subject, Statistic
from core.utils import aggregate_subject 


class BaseTestCase(TestCase):
    fixtures = ['logan_square_test_data.json']

    def setUp(self):
        pass

    def tearDown(self):
        pass

class AggregationTestCase(BaseTestCase):
    def test_data(self):
        """ Make sure our test data hasn't changed """
        self.assertEqual(Neighborhood.objects.all().count(), 1)
        self.assertEqual(CensusBlock.objects.all().count(), 1207)
        self.assertEqual(Subject.objects.all().count(), 1)
        self.assertEqual(Statistic.objects.all().count(), 1207)

        self.assertEqual(Neighborhood.objects.all()[0].name, 'Logan Square')
        blocks = CensusBlock.objects.filter(geoid10__in=('170312216002019', '170312215002012', '170312214002010'))
        self.assertEqual(blocks.count(), 3)

        for block in blocks:
            self.assertEqual(block.statistic_set.count(), 1)
            self.assertEqual(block.statistic_set.all()[0].subject.name, 'Total Population')
            self.assertIn(str(block.statistic_set.all()[0].value), ('13.0000', '37.0000', '91.0000'))
         
    def test_aggregate_subject(self):
        """
        Tests aggregating a subject from Census Blocks to Nieghborhoods 
        """
        subject = Subject.objects.get(name='Total Population')
        aggregate_subject(subject, CensusBlock.objects.filter(geoid10__in=('170312216002019', '170312215002012', '170312214002010')), Neighborhood.objects.all())
        neighborhood = Neighborhood.objects.get(name='Logan Square')
        self.assertEqual(neighborhood.statistic_set.get(subject=subject).value, Decimal('141.0000'))
