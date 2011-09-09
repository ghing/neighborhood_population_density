from django.contrib.gis import admin
from core.models import Neighborhood, CensusBlock, Subject, Statistic

admin.site.register(Neighborhood, admin.OSMGeoAdmin)
admin.site.register(CensusBlock, admin.OSMGeoAdmin)
admin.site.register(Subject, admin.OSMGeoAdmin)
admin.site.register(Statistic, admin.OSMGeoAdmin)
