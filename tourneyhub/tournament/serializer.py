from rest_framework import serializers
from . models import TournamentInfo

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentInfo
        fields = ['title', 'description', 'location', 'date', 'time', 'address', 'registration_fees', 'first_price', 'second_price', 
                  'num_of_teams', 'poster']