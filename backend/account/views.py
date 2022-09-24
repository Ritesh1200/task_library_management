from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from account.serializers import UserSerializer
from account import models
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class Login(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)

        if not email or not password:
            return Response({"data":"","error":"email and password is required"}, status=400)

        user = authenticate(email = email, password = password)
        if user:
            login(request, user)
            user_serial = UserSerializer(user)
            return Response({"data":user_serial.data, "is_librarian":user.is_superuser, "error":""}, status=200)
        return Response({"data":"","error":"email and password is incorrect"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class Registration(APIView):
    def post(self, request):
        
        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)
        name = data.get("name", None)
        is_superuser = data.get("is_superuser", False)
        print(request.data) 
        if not email or not password or not name:
            return Response({"data":"","error":"email and password and name is required"}, status=400)
        user = models.User.objects.filter(email = email).first()
        if user:
            return Response({"data":"","error":"email is already used"}, status=400)

        push_data = {
            "email":email,
            "password":make_password(self.request.data['password']),
            "name": name,
            "is_active":True,
            "is_superuser":is_superuser
        }
        user_serial = UserSerializer(data= push_data)
        user_serial.is_valid(raise_exception=True)
        user_serial.save()
        print(user_serial.data)
        user = models.User.objects.filter(pk = user_serial.data["id"]).first()
        return Response({"data":user_serial.data, "is_librarian":user.is_superuser,  "error":""}, status=200)

class Student(generics.ListAPIView):
    queryset = models.User.objects.filter(is_superuser = False).order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


