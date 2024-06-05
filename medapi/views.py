from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from shop.models import Medicine
from medapi.serializers import MedicineSerializer
from django.contrib.auth.forms import UserCreationForm
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

# Signup API view
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        return Response("account created successfully", status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API view
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

# Create Medicine API view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medicine(request):
    serializer = MedicineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve Medicine API view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_medicine(request):
    try:
        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine, many=True)
        return Response(serializer.data)
    except Medicine.DoesNotExist:
        return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)

# Update Medicine API view
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine(request, pk):
    medicine = get_object_or_404(medicine, pk=pk)
    serializer = MedicineSerializer(request.data, instance=medicine)
    if serializer.is_valid():
        serializer.save()
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Medicine API view
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medicine(request, pk):
    try:
        medicine = Medicine.objects.get(pk=pk, user=request.user)
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Medicine.DoesNotExist:
        return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)