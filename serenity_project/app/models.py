from email.policy import default
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
    gradeCount = models.FloatField(default=0, max_length=10)
    userAvg = models.FloatField(default=0, max_length=10)
    userGrade = models.FloatField(default=0, max_length=10)

    def __str__(self):
        return f"Zipcode: {self.zipcode}, Score: {self.residentialNoise}, Grade:"

    # def serenity_score(self):
    #     return str(self.residential_Noise)



# class Forum(model.Model): 
    """
    zipcode

    """
    

#parent model
class ForumPost(models.Model): # change to ForumPost foreign key to Forum
    id = models.AutoField(primary_key=True)
    zipcode = models.ForeignKey(ScoreTable, blank=True, on_delete=models.CASCADE, default=1, null=True)
    name=models.CharField(max_length=200,default="anonymous" )
    email=models.CharField(max_length=200,null=True)
    topic= models.CharField(max_length=300)
    description = models.CharField(max_length=1000,blank=True)
    # link = models.CharField(max_length=100 ,null =True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return str(self.topic)
 
#child model
class Comment(models.Model): # change to Comment
    id = models.AutoField(primary_key=True)
    forumPost = models.ForeignKey(ForumPost,blank=True,on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
 
    def __str__(self):
        return str(self.forumPost)