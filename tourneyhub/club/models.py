from django.db import models
from django.conf import settings

class Club(models.Model):
    club_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    president = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,related_name='president_club', null= True)
    vice_president = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='vice_president_club', null= True)
    treasurer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='treasurer_club', null= True)
    secretary = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='secretary_club', null= True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='created_by_club', null= True)

    def __str__(self):
        return self.club_name
