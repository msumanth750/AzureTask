from django.db import models

# Create your models here.
class TaskStatus(models.Model):
    name = models.CharField(max_length=100,unique=True)
    code = models.CharField(max_length=15)

    def __str__(self):
        return self.name
class TaskLevel(models.Model):
    name = models.CharField(max_length=100,unique=True)
    code = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Timestampmodel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract =True


class Task(Timestampmodel):
    created_by = models.ForeignKey('account.User',on_delete=models.CASCADE ,related_name='created_user')
    updated_by = models.ForeignKey('account.User',on_delete=models.CASCADE ,related_name='updated_user')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    level = models.ForeignKey('TaskLevel',on_delete=models.CASCADE,related_name='levels')
    status = models.ForeignKey('TaskStatus',on_delete=models.CASCADE,related_name='status',null=True)
    org = models.ForeignKey('account.Organisation',on_delete=models.CASCADE ,related_name='org_tasks')
    project = models.ForeignKey('account.Project',on_delete=models.CASCADE ,related_name='projects')
    org = models.ForeignKey('account.Organisation',on_delete=models.CASCADE ,related_name='org_tasks')
    assigned_to = models.ForeignKey('account.User',null=True,blank=True ,on_delete=models.CASCADE ,related_name='assignee')
    azure = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.title

class SubTask(Timestampmodel):
    created_by = models.ForeignKey('account.User',on_delete=models.CASCADE ,related_name='screated_user')
    updated_by = models.ForeignKey('account.User',on_delete=models.CASCADE ,related_name='supdated_user')
    parent = models.ForeignKey('Task',on_delete=models.CASCADE ,related_name='parent_task')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    status = models.ForeignKey('TaskStatus',on_delete=models.CASCADE,related_name='sstatus',null=True)

    assigned_to = models.ForeignKey('account.User',null=True,blank=True ,on_delete=models.CASCADE ,related_name='subtask_assignee')
    azure = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.title

class TaskComment(Timestampmodel):
    task = models.ForeignKey('Task',on_delete=models.CASCADE ,related_name='task')
    subtask = models.ForeignKey('SubTask',on_delete=models.CASCADE ,related_name='child_task',null=True)
    created_by = models.ForeignKey('account.User',on_delete=models.CASCADE ,related_name='commented_user')
    updated_by = models.ForeignKey('account.User',on_delete=models.CASCADE ,related_name='commented_updateuser')
    description = models.TextField()
    level = models.IntegerField(default =1)
    active = models.BooleanField(default=True)

from PIL import Image, ImageOps
from io import BytesIO
from django.core.files import File
import os

class ImageModel(Timestampmodel):
    task = models.ForeignKey('Task', on_delete = models.CASCADE,related_name='images')
    image = models.ImageField(null=True, default=None,upload_to = 'images/')

    def __str__(self):
        return self.task.title

    # def save(self, *args, **kwargs):
    #   im = Image.open(self.image)
    #   # Convert Image to RGB color mode
    #   im = im.convert('RGB')
    #   # auto_rotate image according to EXIF data
    #   im = ImageOps.exif_transpose(im)
    #   # save image to BytesIO object
    #   im_io = BytesIO()
    #   # save image to BytesIO object
    #   im.save(im_io, 'JPEG', quality=30)
    #
    #   # Change extension      # create a django-friendly Files object
    #   new_image = File(im_io, name='image.jpg')
    #   # Change to new image
    #   self.image = new_image
    #   super().save(*args, **kwargs)


class File(Timestampmodel):
    task = models.ForeignKey('Task', on_delete = models.CASCADE,related_name='files')
    image = models.FileField(null=True, default=None,upload_to = 'files/')


class Note(Timestampmodel):
    task = models.ForeignKey('Task',on_delete=models.CASCADE ,related_name='note_task')
    created_by = models.ForeignKey('account.User',on_delete=models.CASCADE ,related_name='note_user')
    updated_by = models.ForeignKey('account.User',on_delete=models.CASCADE ,related_name='note_updateuser')
    title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.IntegerField(default =1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
