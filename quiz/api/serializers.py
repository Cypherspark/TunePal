from rest_framework import serializers
from account.models import CustomUser as User
from quiz.models import  QuizPassage,QuizImage

class UserScore(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['score']
class Imagequizserializer(serializers.ModelSerializer):
    class Meta:
        model = QuizPassage
        fields = ["question",'choices1','choices2','choices3','choices4']
class passagequizserializer(serializers.ModelSerializer):
    class Meta:
        model = QuizImage
        fields = ["question",'choices1','choices2','choices3','choices4']
class Checkanswer(serializers.ModelSerializer):
            class Meta:
                model = QuizPassage
                fields = ["quiz_id",'answer']
