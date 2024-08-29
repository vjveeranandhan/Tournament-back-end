from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.decorators import ratelimit  # type: ignore
from rest_framework.response import Response
from rest_framework import status
from .serializer import TournamentSerializer
from .models import TournamentInfo
from user_manager.models import CustomUser
# Create your views here.

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def register_tournament(request):
    try:
        print("request.user.id : ", request.user.id)
        if request.method == 'POST':
            if request.user.id:
                serializer = TournamentSerializer(data= request.data, many = False)
                print(serializer.is_valid())
                if serializer.is_valid():
                    print("successfull")
                    created_by = CustomUser.objects.filter(id= request.user.id).first()
                    print("created_by : ", created_by)
                    tournament = TournamentInfo.objects.create(
                    title=serializer.validated_data['title'],
                    description=serializer.validated_data['description'],
                    location=serializer.validated_data['location'],
                    date=serializer.validated_data['date'],
                    time=serializer.validated_data['time'],
                    address=serializer.validated_data['address'],
                    registration_fees=serializer.validated_data['registration_fees'],
                    first_price=serializer.validated_data['first_price'],
                    second_price=serializer.validated_data['second_price'],
                    num_of_teams=serializer.validated_data['num_of_teams'],
                    poster=serializer.validated_data['poster'],
                    created_user_id=created_by)
                    tournament.save() 
                    return Response({"message": "Club creation successfull!"}, status=status.HTTP_201_CREATED)
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({'message': 'Something went wrong please try again later!'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_tournaments(request):
    try:
         if request.method == 'GET':
            if request.user.id:
                tournament_list = TournamentInfo.objects.filter(created_user_id= request.user.id).all()
                serializer = TournamentSerializer(tournament_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid user!"}, status=status.HTTP_400_BAD_REQUEST)
    except:
         return Response({'message': 'Something went wrong please try again later!'}, status=status.HTTP_400_BAD_REQUEST)