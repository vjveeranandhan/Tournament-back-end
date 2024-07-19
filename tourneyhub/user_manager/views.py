from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializer import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django_ratelimit.decorators import ratelimit # type: ignore
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@ratelimit(key='ip', rate='5/m', block=True)
@api_view(['POST'])
def create_user(request):
    try:
        if request.method == 'POST':
            _data = request.data
            if 'email' in _data:
                if CustomUser.objects.filter(email= _data['email']).exists():
                    return Response({"message":"Email alrady exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({"message": "Email is missing"}, status=status.HTTP_404_NOT_FOUND)
            
            if 'phone' in _data:
                if CustomUser.objects.filter(phone= _data['phone']).exists():
                    return Response({"message":"Phone number alrady exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                 return Response({"message": "Phone number is missing"}, status=status.HTTP_404_NOT_FOUND)
            
            if 'age' not in _data:
                return Response({"message": "Age is missing"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(data= _data, many = False)
            if serializer.is_valid():
                user = CustomUser.objects.create(username = serializer.validated_data['username'], email = serializer.validated_data['email'],
                                                 phone = serializer.validated_data['phone'], age = serializer.validated_data['age'])
                user.set_password(serializer.validated_data['password'])
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
        if request.method == 'POST':
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']

                user = authenticate(username=username, password=password)
                
                if user is not None:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
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