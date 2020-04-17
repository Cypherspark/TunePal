from django.db import models

class QuizImage(models.Model):
    question = models.CharField(max_length=500)
    choices1 = models.CharField(max_length = 20)
    choices2 = models.CharField(max_length = 20)
    choices3 = models.CharField(max_length = 20)
    choices4 = models.CharField(max_length = 20, default = None)
    answer = models.CharField(max_length = 20)
    quiz_id = models.CharField(max_length = 200000,blank=True,null = True,default = None)
class QuizPassage(models.Model):
    question = models.CharField(max_length=500)
    choices1 = models.CharField(max_length = 20)
    choices2 = models.CharField(max_length = 20)
    choices3 = models.CharField(max_length = 20)
    choices4 = models.CharField(max_length = 20, default = None)
    answer = models.CharField(max_length = 20)
    quiz_id = models.CharField(max_length = 200000,blank=True,null = True,default = None)
