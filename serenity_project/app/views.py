from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import ScoreTable
from .serializers import ScoreTableSerializer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, Template, Context
import pandas as pd
import numpy as np

class ScoreTableViewSet(viewsets.ModelViewSet):
    queryset = ScoreTable.objects.all()
    serializer_class = ScoreTableSerializer


def index(request):
    latest_zipcode_list = ScoreTable.objects.order_by('zipcode')[:5]
    context = {
        'latest_zipcode_list':latest_zipcode_list
    }
    return render(request, 'app/index.html', context)

def search(request):
    csrfContext = RequestContext(request)
    if request.method == 'POST':
        search = request.POST['searched']
        post = ScoreTable.objects.get(zipcode=search)
       # currZip = post.zipcode
        normalizeNoise = post.residential_Noise / 1000
        if normalizeNoise >= 7:
            post.grade = "G"
        elif normalizeNoise < 7 and normalizeNoise >= 6:
            post.grade = "G"
        elif normalizeNoise < 6 and normalizeNoise >= 5:
            post.grade = "E"
        elif normalizeNoise < 5 and normalizeNoise >= 4:
            post.grade = "D"
        elif normalizeNoise < 4 and normalizeNoise >= 3:
            post.grade = "C"
        elif normalizeNoise < 3 and normalizeNoise >= 2:
            post.grade = "B"
        elif normalizeNoise < 2 and normalizeNoise >= 0:
            post.grade = "A"
        post.residential_Noise = normalizeNoise;
        return render(request, 'app/search.html', {'post' : post})
    else:
        return render(request, 'app/search.html',{},csrfContext)