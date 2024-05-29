from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template import loader

def home(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))