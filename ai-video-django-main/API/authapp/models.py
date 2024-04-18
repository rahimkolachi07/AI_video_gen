# from django.db import models
# from django.contrib.auth.models import AbstractUser

# # # Create your models here.
# # class User(AbstractUser):
# #     name = models.CharField(max_length=255)
# #     email = models.CharField(max_length=255, unique=True)
# #     password = models.CharField(max_length=255)
# #     username = None

# #     USERNAME_FIELD = 'email'
# #     REQUIRED_FIELDS = []

# # class Prompts(models.Model):
# #     userId = models.ForeignKey(User, on_delete=models.CASCADE)
# #     video = models.CharField(max_length=500)

# #     def __str__(self):
# #         return self.id

from django.db import models
from django.contrib.auth.models import User

class Prompts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"{self.user.username}'s URL: {self.url}"