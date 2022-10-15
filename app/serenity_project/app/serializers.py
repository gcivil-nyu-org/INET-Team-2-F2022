from dataclasses import field

from rest_framework import serializers

from .models import ScoreTable


class ScoreTableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ScoreTable
        fields = '__all__'