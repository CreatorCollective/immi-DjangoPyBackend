from django.shortcuts import render

def index(request):
    return render(request, 'opt/index.html', {})

# Create your views here.
