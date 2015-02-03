from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from Table.models import Person


@require_GET
def get_data(request):
    tmpl = "base.html"
    persons = Person.objects.all()[:10]
    context = {'persons': persons}
    return render_to_response(tmpl, context)