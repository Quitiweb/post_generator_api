from django.http import HttpResponse
import datetime
from django.template import Template, Context


def home(request):

    return HttpResponse('holaaaaaaaaa')