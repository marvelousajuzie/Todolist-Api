from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import CustomUserserializer, UserLoginSerializer, Todolistserializer
from rest_framework.authentication import TokenAuthentication
from .pagination import Todolistpagination
from rest_framework.authtoken.models import Token
from .models import CustomUser, TodoList
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate


class CustomUserRegister(viewsets.ModelViewSet):
        serializer_class = CustomUserserializer

        def post_queryset(self):
            return []
        
        def create(self, request):
            serializer = self.get_serializer_class(data= request.data)
            if serializer.is_valid():
                serializer.save()
                user = serializer.data
                return Response({
                'data': user
            }, status= status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CustomUserLogin(viewsets.ModelViewSet):

    serializer_class = UserLoginSerializer

    def post_queryset(self):
        return []
    
    def create(self, request):
        serializer = self.get_serializer_class(data= request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email = email, password=password)
            if user is not None:
                token,_ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status= status.HTTP_200_OK)
            else:
                return Response({'Invalid Credidentials'}, status= status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    

class TodoView(viewsets.ModelViewSet):
    authentication_classes =  [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Todolistserializer
    queryset = TodoList.objects.all()
    
    def list(self, request):
        query_set =TodoList.objects.filter(user= request.user)
        paginator = Todolistpagination()
        page = paginator.paginate_queryset( query_set, request)
        serializer = self.get_serializer_class(page, many= True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer_class(data= request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, pk= None):
        try:
            query_set = TodoList.objects.get(id = pk, user= request.user)
        except TodoList.DoesNotExist:
            return Response({'message': 'Item does not exist'}, status= status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer_class(query_set,  data= request.data, partial= True)
        if serializer.is_valid():
            serializer.save(user= request.user)
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
   
    def destroy(self, request, pk= None):
        query_set = TodoList.objects.get(id=pk, user= request.user)
        TodoList.delete(query_set)
        return Response({'message': 'Todolit Deleted Sucessfully'}, status= status.HTTP_200_OK)
    

    
        
