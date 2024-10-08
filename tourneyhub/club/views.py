from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django_ratelimit.decorators import ratelimit # type: ignore
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from . club_data_validation  import validate_club_data
from . serializer import ClubSerializer, GetClubSerializer
from . models import Club
from user_manager.models import CustomUser

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def register_club(request):
    try:
        if request.method == 'POST':
            _data = request.data
            if request.user.id:
                _data['user_id'] = request.user.id
                validation_check_response = validate_club_data(_data, 'club-registration')
                print(" validation_check_response ", validation_check_response)   
                if validation_check_response[0] ==  False:
                        check_status_response = validation_check_response[1]
                        return Response({"message":check_status_response}, status=status.HTTP_406_NOT_ACCEPTABLE)
                serializer = ClubSerializer(data= _data, many = False)
                if serializer.is_valid():
                    print("successfull")
                    created_by = CustomUser.objects.filter(id= _data['user_id']).first()
                    club = Club.objects.create(club_name= serializer.validated_data['club_name'], country= serializer.validated_data['country'],
                                                    state = serializer.validated_data['state'], district = serializer.validated_data['district'],
                                                    phone = serializer.validated_data['phone'],  email= serializer.validated_data['email'], 
                                                    description= serializer.validated_data['description'], created_by = created_by)
                    club.save()
                    return Response({"message": "Club creation successfull!"}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors)
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({'message': 'Something went wrong please try again later!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_club(request):
    try:
         if request.method == 'GET':
            data = {}
            if request.user.id:
                data['user_id'] = request.user.id
                validation_status_and_data = validate_club_data(data, 'fetch-club')
                if validation_status_and_data[0]:
                    serializer = GetClubSerializer(validation_status_and_data[1])
                    return Response({'status': 'club found', 'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    if (validation_status_and_data[0] == False) and (validation_status_and_data[1] == 'Club not found'):
                        return Response({'status': 'club not found', 'data': ''}, status=status.HTTP_200_OK)
                    return Response({"message": "User id is missing!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "User id is missing!"}, status=status.HTTP_400_BAD_REQUEST)
    except:
         return Response({'message': 'Something went wrong please try again later!'}, status=status.HTTP_400_BAD_REQUEST)