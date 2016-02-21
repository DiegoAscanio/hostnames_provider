from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from .models import Host

# Create your views here.

def index(request):
    ip = request.META['REMOTE_ADDR']
    h = Host.objects.get(ip_address=ip)
    return HttpResponse(h.hostname)
