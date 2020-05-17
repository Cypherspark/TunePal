from django.db import models

class QuizImage(models.Model):
    question = models.CharField(max_length=500)
    choices1 = models.CharField(max_length = 200)
    choices2 = models.CharField(max_length = 200)
    choices3 = models.CharField(max_length = 200)
    choices4 = models.CharField(max_length = 200, default = None)
    answer = models.CharField(max_length = 200)
    quiz_id = models.CharField(max_length = 200000,blank=True,null = True,default = None)
class QuizPassage(models.Model):
    question = models.CharField(max_length=700)
    choices1 = models.CharField(max_length = 200)
    choices2 = models.CharField(max_length = 200)
    choices3 = models.CharField(max_length = 200)
    choices4 = models.CharField(max_length = 200, default = None)
    answer = models.CharField(max_length = 200)
    quiz_id = models.CharField(max_length = 200000,blank=True,null = True,default = None)
