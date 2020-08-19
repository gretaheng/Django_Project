# Original Code

from django.http import HttpResponse
from django.shortcuts import render

def ana(request):
    return render(request, 'analysis/analysis.html')