from django.shortcuts import render
from api.serializers import UserSerializer,ProfileSerializer,QuestionSerializer,AnswerSerializer
from rest_framework.response import Response
from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet,GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from stack.models import UserProfile,Questions,Answer
from rest_framework import authentication,permissions
from rest_framework.decorators import action

# Create your views here.
class UsersView(GenericViewSet,CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class ProfileView(ModelViewSet):

    serializer_class=ProfileSerializer
    queryset=UserProfile.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return UserProfile.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        prof=self.get_object()
        if prof.user !=request.user:
            raise serializers.ValidationError("not allowed to perform")
        else:
            return super().destroy(request,*args,**kwargs)
    
    # def list(self,request,*args,**kwargs):
    #     qs=UserProfile.objects.get(user=request.user)
    #     serializer=ProfileSerializer(qs,many=False)
    #     return Response(data=serializer.data)
    # def create(self, request, *args, **kwargs):
    #     serializer=ProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

class QuestionView(ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # def get_queryset(self):
        # return Questions.objects.all().order_by("-created_date")
    @action(methods=["post"],detail=True)
    def add_answer(self,request,*args,**kwargs):
        serializer=AnswerSerializer(data=request.data)
        quest=self.get_object()
        user=request.user
        if serializer.is_valid():
            serializer.save(question=quest,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
from rest_framework import serializers
class AnswerView(ModelViewSet):
    serializer_class=AnswerSerializer
    queryset=Answer.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("method not allowed")
    @action(methods=["post"],detail=True)
    def add_upvote(self,request,*args,**kwargs):
        answer=self.get_object()
        answer.upvote.add(request.user)
        answer.save()
        return Response(data="upvoted")
    
    @action(methods=["post"],detail=True)
    def down_upvote(self,request,*args,**kwargs):
        answer=self.get_object()
        answer.upvote.remove(request.user)
        answer.save()
        return Response(data="upvoted removed")
    


    