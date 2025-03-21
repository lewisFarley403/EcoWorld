from django.db import models

from Accounts.models import User


# Create your models here.

class ContentQuizPair(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    quiz_questions = models.JSONField()
    quiz_max_marks = models.IntegerField(default=-1)
    reward = models.IntegerField(default=50)

    def __str__(self):
        return self.title

class UserQuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_quiz_pair = models.ForeignKey(ContentQuizPair, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    best_result = models.IntegerField(default=0)
    previous_best = models.IntegerField(default=0)
    date_taken = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Automatically set is_completed to True if the user scores 100%
        if self.score == self.content_quiz_pair.quiz_max_marks:
            self.is_completed = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.content_quiz_pair.title}"