from django.db import models

# Create your models here.

class ScoreTable(models.Model):
    zipcode = models.IntegerField()
    crime_score = models.FloatField(max_length=10)
    tree_score = models.FloatField(max_length=10)

    def __str__(self):
        return str(self.zipcode)