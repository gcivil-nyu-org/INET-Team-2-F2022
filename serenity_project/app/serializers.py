from dataclasses import field
from rest_framework import serializers
from .models import ScoreTable, ForumPost


class ScoreTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreTable
        fields = "__all__"

class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = "__all__"