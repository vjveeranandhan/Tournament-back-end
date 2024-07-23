from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializer import UserSerializer, LoginSerializer, UserRetrieveSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django_ratelimit.decorators import ratelimit # type: ignore
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import date
from . user_data_validation import validate_user_data


@ratelimit(key='ip', rate='5/m', block=True)
@api_view(['POST'])
def create_user(request):
    try:
        if request.method == 'POST':
            check_status = validate_user_data(request.data)[0]
            if check_status ==  False:
                check_status_response = validate_user_data(request.data)[1]
                return Response({"message":check_status_response}, status=status.HTTP_406_NOT_ACCEPTABLE)
            _data = request.data
            serializer = UserSerializer(data= _data, many = False)
            if serializer.is_valid():
                user = CustomUser.objects.create(first_name= serializer.validated_data['first_name'], last_name= serializer.validated_data['last_name'],
                                                username = serializer.validated_data['username'], email = serializer.validated_data['email'],
                                                phone = serializer.validated_data['phone'], date_of_birth= serializer.validated_data['date_of_birth'], age= serializer.validated_data['age'])
                user.set_password(_data['password'])
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        else:
            return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)

@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['POST'])
def user_login(request):
    try:
        print(request.data)
        if request.method == 'POST':
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']

                user = authenticate(username=username, password=password)
                
                if user is not None:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Method Not Allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Succesfully Logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        if request.user.is_authenticated:
            user = CustomUser.objects.filter(id=request.user.id).first()
            serializer = UserRetrieveSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)