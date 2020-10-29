from django.db import models
from PIL import Image

class Club(models.Model):
    name = models.TextField(max_length=100) # real name of club
    screen_name = models.CharField(max_length=100) # tweeter screen-name of club official profile
    image = models.ImageField(default='img.png', upload_to='img')

    def __str__(self):
        return self.name

#model Services:
#SkySportsPL
#premierleague