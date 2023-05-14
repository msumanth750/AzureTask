from django.shortcuts import render
from tasks.models import Task
from account.models import Project
# Create your views here.
def index(request):
    projects = Project.objects.all()
    return render(request,'fe/index.html',{'projects':projects})

def tasks(request):
    tasks = Task.objects.all()
    return render(request,'fe/tables.html',{'tasks':tasks})
