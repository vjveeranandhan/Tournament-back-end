from rest_framework import serializers
from . models import Club

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['club_name', 'country', 'state', 'district', 'phone', 'email', 'description']

class GetClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['club_name', 'description', 'country', 'state', 'district', 'phone', 'email', 'president', 'vice_president', 'treasurer']