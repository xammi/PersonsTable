from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST, require_http_methods


@require_GET
def get_data(request):
    tmpl = "base.html"
    context = {}
    return render_to_response(tmpl, context)