# coding: utf-8

from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest
from json import dumps
from django.core.exceptions import ObjectDoesNotExist

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


def response_json(response):
    obj = {'status': 'OK', 'data': response}
    return HttpResponse(dumps(obj), content_type="application/json")


def response_error(response):
    obj = {'status': 'error', 'errors': response}
    return HttpResponse(dumps(obj), content_type="application/json")

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
    persons = Person.objects.all()[:]
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

    return response_error(form.errors)


@require_AJAX
@require_POST
def update_person(request):
    p_id = request.POST['id']
    field = request.POST['field']
    new_value = request.POST['new_value']

    if not p_id or not field or not new_value:
        msg = '''Update can not be done without id, field or new_value'''
        return response_error({'Missed parameter': msg})

    if field not in Person.fields():
        msg = '''Unknown field in person model (%s)''' % field
        return response_error({'Unknown field': msg})

    form = AddPersonForm()
    if not form.is_field_valid(field, new_value):
        msg = '''Invalid new_value (%s) for field (%s)''' % (new_value, field)
        return response_error({'Invalid value': msg})

    try:
        person = Person.objects.all().get(id=int(p_id))
        person.__dict__[field] = new_value
        person.save(force_update=True)
        return response_json({'id': person.id, 'values': person.as_dict()})

    except ObjectDoesNotExist:
        msg = '''No person record with such id in DB (id=%s)''' % p_id
        return response_error({'Does not exist': msg})

    except TypeError:
        msg = '''id must be integer (id=%s)''' % p_id
        return response_error({'Wrong type': msg})


@require_AJAX
@require_POST
def delete_persons(request):
    ids = request.POST['ids']

    if not ids or ids == '':
        msg = '''Unable to delete persons without id list'''
        return response_error({'Missed parameter': msg})

    try:
        int_ids = [int(p_id) for p_id in ids.split(',')]

        for p_id in int_ids:
            person = Person.objects.all().get(id=p_id)
            person.delete()
        return response_json({'ids': ids})

    except ObjectDoesNotExist:
        msg = '''No person record with such id in DB'''
        return response_error({'Does not exist': msg})

    except TypeError:
        msg = '''ids must be integers (ids = [%s])''' % ids
        return response_error({'Wrong type': msg})