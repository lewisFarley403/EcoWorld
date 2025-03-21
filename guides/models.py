from django.db import models
from Accounts.models import User

# Create your models here.

"""
This class represents a content and quiz pair, which includes 
educational content and associated quiz questions.

Attributes:
    title (CharField): 
        The title of the content-quiz pair.
    content (TextField): 
        The main content or educational material.
    quiz_questions (JSONField): 
        A JSON field containing the quiz questions and answers.
    quiz_max_marks (IntegerField): 
        The maximum marks achievable in the quiz. Default is -1.
    reward (IntegerField): 
        The coins given for completing the quiz. Default is 50.

Returns:
    str: The title of the content-quiz pair when the object is printed.

author:
    Johnny Say (js1687@exeter.ac.uk)
"""
class ContentQuizPair(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    quiz_questions = models.JSONField()
    quiz_max_marks = models.IntegerField(default=-1)
    reward = models.IntegerField(default=50)

    def __str__(self):
        return self.title


"""
This class represents the result of a user's attempt at a quiz 
associated with a content-quiz pair.

Attributes:
    user (ForeignKey): 
        A reference to the User who took the quiz.
    content_quiz_pair (ForeignKey): 
        A reference to the ContentQuizPair associated with the quiz.
    score (IntegerField): 
        The score achieved in the quiz. Default is 0.
    best_result (IntegerField): 
        The best score achieved for this quiz. Default is 0.
    previous_best (IntegerField): 
        The previous best before the current attempt. Default is 0.
    date_taken (DateTimeField): 
        The date and time when the quiz was taken. 
        Set to the current time when the object is created.
    is_completed (BooleanField): 
        Whether the quiz was completed with 100%. Default is False.

Methods:
    save: Overrides the save method to automatically set is_completed 
    to True if the user scores 100%.

Returns:
    str: A string of the user and the content-quiz pair title.

author:
    Johnny Say (js1687@exeter.ac.uk)
"""
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