from django.shortcuts import render
from tasks.models import Task

# Create your views here.
def index(request):
    return render(request,'fe/index.html')

def tasks(request):
    tasks = Task.objects.all()
    return render(request,'fe/tables.html',{'tasks':tasks})
