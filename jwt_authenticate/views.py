from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .token_gen_validate import generate_access_token, generate_refresh_token
from rest_framework import status

@api_view(['GET'])
@permission_classes[AllowAny]
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response('Invalid Credentials!')
    
    acess_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    payload = {
        'user_id': user.id,
        'user_email': user.email,
        'access': acess_token,
        'refresh': refresh_token
    }
    return Response(payload, status=status.HTTP_200_OK)