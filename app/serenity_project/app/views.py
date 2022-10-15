from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import ScoreTable
from .serializers import ScoreTableSerializer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

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
        post = ScoreTable.objects.filter(zipcode=search)
        return render(request, 'app/search.html', {'post' : post},csrfContext)
    else:
        return render(request, 'app/search.html',{},csrfContext)