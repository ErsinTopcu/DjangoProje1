from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting


def index(request):
    settig = Setting.objects.get(pk=1)
    context = {'setting': settig}
    return render(request, 'index.html', context)
