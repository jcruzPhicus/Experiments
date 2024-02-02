from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")


def other_view(request):
    return render(request, "other_view.html")