
from rest_framework.decorators import api_view
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser

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
            print("Here", serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        else:
            return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)
