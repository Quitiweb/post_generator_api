from django.http import HttpResponse
import datetime
from django.template import Template, Context


def home(request):

    return HttpResponse('Muy buenas ahora mismo se encuentra en la pagina home si desea hacer algo con la API porfavor ponga /admin seguido de la url que tiene ahora mismo')