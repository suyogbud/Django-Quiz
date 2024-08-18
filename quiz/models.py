import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#model for the quiz questions
class Question(models.Model):
    def __str__(self):
        return self.question_text

    #method to check if the question was published recently
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1)<= self.pub_date <= now

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

#model for the choices
class Choice(models.Model):

    def __str__(self):
        return self.choice_text
    #foreign key to the question model
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    #field to store the number of votes
    votes = models.IntegerField(default=0)
    #boolean field to check if the choice is correct
    correct = models.BooleanField(default=False)

class UserScore(models.Model):
    #foreign key to the user model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #field to store the score
    score = models.FloatField()
    #field to store the date the score was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.score}"