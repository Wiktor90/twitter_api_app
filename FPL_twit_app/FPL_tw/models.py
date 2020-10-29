from django.db import models

class Club(models.Model):
    name = models.TextField(max_length=100) # real name of club
    screen_name = models.CharField(max_length=100) # tweeter screen-name of club official profile
    kind = models.CharField(max_length=100, default="club")

    def __str__(self):
        return self.name