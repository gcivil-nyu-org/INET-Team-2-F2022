from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets

from .models import ScoreTable
from .serializers import ScoreTableSerializer


class ScoreTableViewSet(viewsets.ModelViewSet):
    queryset = ScoreTable.objects.all()
    serializer_class = ScoreTableSerializer