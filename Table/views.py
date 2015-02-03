from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import HttpResponse
from Table.models import Person
from django.core.serializers import serialize
import json


@require_GET
def index(request):
    tmpl = "base.html"
    context = {}
    return render_to_response(tmpl, context)


@require_GET
def get_data(request):
    persons = Person.objects.all()[:10]
    response = [{'id': person.id, 'values': person.as_dict()} for person in persons]
    return HttpResponse(json.dumps(response), mimetype="application/json")