from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import HttpResponse
from Table.models import Person
from django.http import HttpResponseBadRequest
from json import dumps
import re

def require_AJAX(view):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return view(request, *args, **kwargs)

    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap


def prepare(queryset, predicate):
    result = [{'id': query.id, 'values': query.as_dict()}
              for query in queryset if predicate(query)]
    return result


def response_json(obj):
    return HttpResponse(dumps(obj), mimetype="application/json")

#--------------------------------------------------------------------------------------------------


@require_GET
def index(request):
    tmpl = "base.html"
    context = {}
    return render_to_response(tmpl, context)


@require_AJAX
@require_GET
def get_data(request):
    filter = request.GET['filter']

    if not filter is None and filter != '':
        pattern = re.compile(filter)
        matcher = lambda person: person.match_to(pattern)
    else:
        matcher = lambda person: True

    persons = Person.objects.all()[:10]
    data = prepare(persons, matcher)
    return response_json(data)


@require_AJAX
@require_POST
def add_person(request):
    new_person = Person()
    new_person.save(force_insert=True)
    return response_json(new_person.as_dict())


@require_AJAX
@require_POST
def update_person(request):
    id = request.POST['id']
    field = request.POST['field']
    new_value = request.POST['new_value']

    person = Person.objects.all().filter(id=id)
    person[field] = new_value
    person.save(force_update=True)

    new_person = Person()
    new_person.save()
    return response_json(new_person.as_dict())


@require_AJAX
@require_POST
def delete_persons(request):
    ids = request.POST['ids']
    for id in ids:
        person = Person.objects.all().filter(id=id)
        person.delete()

    return response_json({'status': 'OK'})