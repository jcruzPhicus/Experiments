from django.shortcuts import render

# Create your views here.
async def index(request):
    return render(request, "index.html")


async def other_view(request):
    return render(request, "other_view.html")