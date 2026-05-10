from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .token_gen_validate import generate_access_token, generate_refresh_token
from rest_framework import status
from .models import task, taskSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .authenticate import CustomJWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class listView(APIView):
    def get(self, request):
        tasks = task.objects.all()
        taskSer = taskSerializer(tasks, many=True)
        return Response(taskSer.data)
    
    def post(self, request):
        taskSer = taskSerializer(data=request.data)
        if taskSer.is_valid():
            taskSer.save()
            return Response(taskSer.data)
        return Response('Authentication Failed!')
    

class detailView(APIView):
    def get(self, request, pk):
        try:
            tasks = task.objects.get(pk)
        except task.DoesNotExist:
            return Response('Task not found!')
        
        taskSer = taskSerializer(request.data, many=False)
        return Response(taskSer.data)
    
    def post(self, request, pk):
        tasks = task.objects.get(pk)
        taskSer = taskSerializer(tasks, data=request.data)
        if taskSer.is_valid():
            taskSer.save()
            return Response(taskSer.data)
        return Response('Invalid data!')

    def delete(self, request, pk):
        tasks = task.objects.get(pk)
        tasks.delete()
        return Response('Task deleted successfully!')


class Register(APIView):
    permission_classes = []

    def post(self, request):
        self.username = request.data.get('username')
        self.password = request.data.get('password')
        self.email = request.data.get('email')

        if User.objects.filter(username=self.username).exists():
            return Response('User already exists for this username!')
        else:
            user = User.objects.create(username=self.username, password = self.password, email=self.email)
            access = generate_access_token(user)
            refresh = generate_refresh_token(user)

            context = {
                'access': access,
                'refresh': refresh, 

            }
            return Response(context, status=status.HTTP_201_CREATED)


class Login(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)

        if not user:
            return Response('No such user! Try again!')
        else: 
            context = {
                'refresh': generate_refresh_token(user),
                'access': generate_access_token(user)
            }
            return Response(context)


class Profile(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        return Response ({
            'id': user.id,
            'usename': user.username,
            'email': user.email

        }, status=status.HTTP_200_OK)
    
        '''self.username = request.data.get('username')
        try: 
            user = User.objects.get(username=self.username)
        except User.DoesNotExist:
            raise AuthenticationFailed('User does not exist!')
        
        self.user = User.objects.get(username=self.username)
        
        return Response({'username': self.user.username, 'id': self.user.id, 'email': self.user.email})
'''