from django.db import models

# Create your models here.

class ScoreTable(models.Model):
    zipcode = models.IntegerField()
    residential_Noise = models.FloatField(max_length=10)

    def __str__(self):
        return f"Zipcode: {self.zipcode}, Score: {self.residential_Noise}"
    # def serenity_score(self):
    #     return str(self.residential_Noise)