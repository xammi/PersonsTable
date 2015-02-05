# coding: utf-8

from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest
from json import dumps

from Table.models import *
from Table.forms import *


def require_AJAX(view):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return view(request, *args, **kwargs)

    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap


def response_json(obj):
    return HttpResponse(dumps(obj), content_type="application/json")


def response_error(msg):
    return HttpResponseBadRequest(msg)

#--------------------------------------------------------------------------------------------------

@require_GET
@ensure_csrf_cookie
def index(request):
    tmpl = "base.html"
    context = RequestContext(request)
    return render_to_response(tmpl, context)


@require_AJAX
@require_GET
def get_data(request):
    persons = Person.objects.all()[:10]
    data = [{'id': person.id, 'values': person.as_dict()}
              for person in persons]
    return response_json(data)


@require_AJAX
@require_POST
def add_person(request):
    data = dict(request.POST.iteritems())
    data['phone'] = data['phone'][1:]
    form = AddPersonForm(data)

    if form.is_valid():
        new_person = Person()

        for field in Person.fields():
            new_person.__dict__[field] = form.cleaned_data[field]

        new_person.save(force_insert=True)
        return response_json(new_person.as_dict())

    errors = form.errors
    return response_error(errors)


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