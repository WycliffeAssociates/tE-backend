from django.shortcuts import render
from api.models import Take

def index(request):
    take = Take.objects.all().last()
    return render(request, 'index.html', {"lasttake": take})