from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import ScoreTable
from .serializers import ScoreTableSerializer
from django.shortcuts import render

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
    if request.method == 'GET':
        search = request.GET.get('search')
        post = ScoreTable.objects.all().filter(zipcode=search)
        return render(request, 'app/index/search.html', {'post' : post})