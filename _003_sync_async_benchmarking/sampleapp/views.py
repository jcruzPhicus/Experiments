from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.

def sync_view(request):
    return HttpResponse(request.headers)

async def async_view(request):
    return HttpResponse(request.headers)