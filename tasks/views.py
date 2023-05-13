from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import Task,TaskComment,Note,ImageModel,File,TaskStatus
from .serializers import (TaskSerializer,
                        TaskCommentSerializer,
                        NoteSerializer,
                        ImageSerializer,
                        FileSerializer,TaskStatusListSerializer,)

from account.models import Profile
# Create your views here.
class TaskView(viewsets.ModelViewSet):
    """
    rest api modelviewset to get ,post ,put,patch the Task model

    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        print(user)
        user_type = user.type
        if user_type.name=="Client":
            queryset = queryset.filter(org = user.org)
        if user_type.name=="Employee":
            queryset=queryset.filter(project__in=user.project.all())
        if user_type.name=='Admin':
            queryset=queryset
        # if user:
        #     queryset = queryset.filter(created_by=user)
        # print(user)
        return queryset
    def list(self,request):
        queryset = self.get_queryset()
        values = queryset.values('id','title','description','status__name','level__name','project__name','created_by__name')
        return Response(values)


class TaskCommentView(viewsets.ModelViewSet):
    """
    model viewset for the model TaskComment model
    """
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer

class NoteView(viewsets.ModelViewSet):
    """
    model viewset for the model NoteView
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class ImageView(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class =FileSerializer

class TaskStatusListView(viewsets.ModelViewSet):
    queryset =TaskStatus.objects.all()
    serializer_class = TaskStatusListSerializer
