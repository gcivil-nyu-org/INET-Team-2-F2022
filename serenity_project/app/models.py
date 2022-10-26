from django.db import models

# Create your models here.


class ScoreTable(models.Model):
    id = models.AutoField(primary_key=True)
    zipcode = models.IntegerField()
    residentialNoise = models.FloatField(max_length=10)
    dirtyConditions = models.FloatField(max_length=10)
    sanitationCondition = models.FloatField(max_length=10)
    wasteDisposal = models.FloatField(max_length=10)
    unsanitaryCondition = models.FloatField(max_length=10)
    grade = "A"

    def __str__(self):
        return f"Zipcode: {self.zipcode}, Score: {self.residentialNoise}, Grade:"

    # def serenity_score(self):
    #     return str(self.residential_Noise)
