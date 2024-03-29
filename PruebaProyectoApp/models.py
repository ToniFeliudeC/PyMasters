from django.db import models
from django.contrib.auth.models import User


class Challenge(models.Model):
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    description = models.TextField()
    code_template = models.TextField()
    test_cases = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.IntegerField(default=1)
    category = models.TextField(default="")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date_solved = models.DateTimeField(auto_now_add=True)
    solution = models.TextField(default=None)
    

    class Meta:
        unique_together = ["user", "challenge", "solution"]

    def __str__(self):
        return f'{self.user.username} - {self.challenge.title}'


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.score}'


class Comment(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(default='Empty comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.body[:50]}'
    

class Response(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.body[:50]}'

# class Solution(models.Model):
#     challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='solutions')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     code = models.TextField()
#     passed_tests = models.IntegerField()
#     total_tests = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} - {self.challenge.title}'
