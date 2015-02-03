import os
os.environ["DJANGO_SETTINGS_MODULE"] = "PersonsTable.settings"

from Table.models import Person

def clear_all():
    Person.objects.all().delete()
    print "DB was cleared successfully"

clear_all()
