from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import HttpResponse
from Table.models import Person
from django.http import HttpResponseBadRequest
import json
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

    persons = Person.objects.all()
    response = prepare(persons, matcher)
    return HttpResponse(json.dumps(response), mimetype="application/json")