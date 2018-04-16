from django.shortcuts import render

from ..file_transfer import FileUtility


def index(request):
    return render(request, 'index.html')
