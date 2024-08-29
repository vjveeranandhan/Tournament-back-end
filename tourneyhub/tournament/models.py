from django.db import models
from user_manager.models import CustomUser

# Create your models here.
class TournamentInfo(models.Model):
    title = models.CharField(max_length= 120)
    # year = models.IntegerField(null= True)
    description = models.TextField()
    location = models.TextField()
    latitude = models.FloatField(null= True)
    longitude = models.FloatField(null= True)
    date = models.DateField()
    time = models.TimeField(auto_now=False, auto_now_add=False)
    address = models.TextField()
    registration_fees = models.IntegerField()
    first_price = models.IntegerField()
    second_price = models.IntegerField()
    num_of_teams = models.IntegerField()
    poster = models.ImageField(upload_to='images/tournament_posters/', null=True)
    created_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)