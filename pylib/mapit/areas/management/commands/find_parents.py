# This script is used after Boundary-Line has been imported to
# associate shapes with their parents. With the new coding
# system coming in, this could be done from a BIG lookup table; however,
# I reckon P-in-P tests might be quick enough...

from django.core.management.base import NoArgsCommand
from mapit.areas.models import Area, Generation

class Command(NoArgsCommand):
    help = 'Find parents for shapes'

    def handle_noargs(self, **options):
        current_generation = Generation.objects.current()
        new_generation = Generation.objects.new()
        if not new_generation:
            raise Exception, "No new generation to be used for import!"

        parentmap = {
            'DIW': 'DIS',
            'CED': 'CTY',
            'LBW': 'LBO',
            'LAC': 'GLA',
            'MTW': 'MTD',
            'UTE': 'UTA',
            'UTW': 'UTA',
            'SPC': 'SPE',
            'WAC': 'WAE',
            'CPC': ('DIS', 'UTA', 'MTD', 'LBO'),
        }
        for area in Area.objects.filter(
            type__in=parentmap.keys(),
            generation_low__lte=new_generation, generation_high__gte=new_generation,
        ):
            for polygon in area.polygons.all():
                try:
                    parent = Area.objects.get(
                        type__in=parentmap[area.type],
                        polygons__polygon__contains=polygon.polygon,
                        generation_low__lte=new_generation, generation_high__gte=new_generation,
                    )
                    print "Parent for %s [%d] (%s) is %s [%d] (%s)" % (area.name, area.id, area.type, parent.name, parent.id, parent.type)
                    break
                except Area.DoesNotExist:
                    raise Exception, "Area %s [%d] (%s) does not have a parent?" % (area.name, area.id, area.type)
            #area.parent = parent
            #area.save()

