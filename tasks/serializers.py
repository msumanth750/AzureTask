from rest_framework import serializers
from .models import Task,TaskComment,Note,ImageModel,File,TaskStatus

from tasks.azure_api import azure_workitem_create,azure_workitem_update


from django.core.files import File
import base64
class ImageSerializer(serializers.ModelSerializer):
    base64_image = serializers.SerializerMethodField()
    class Meta:
        model = ImageModel
        fields = '__all__'

    def get_base64_image(self, obj):
        f = open(obj.image.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data

class TaskSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

    class Meta:
        """docstring for Meta."""
        model = Task
        fields = ('__all__')

    def get_comments(self,obj):
        comments  = TaskComment.objects.filter(task=obj,active=True).order_by('-id')
        return comments.values()

    def get_notes(self , obj):
        notes = Note.objects.filter(task=obj,active=True).order_by('-id')
        return notes.values()

    def get_images(self, obj):
        images = ImageModel.objects.filter(task=obj).order_by('-created_at')
        return images.values('id','image')
    #
    def create(self,validated_data):
        task  =  Task.objects.create(**validated_data)
        title = validated_data.get('title',None)
        description = validated_data.get('description',None)

        request = self.context['request']
        user = request.user
        data = [
         {
         "op": "add",
         "path": "/fields/System.Title",
         "value": title
         },
         # {
         # "op": "add",
         # "path": "/fields/System.Description",
         # # "from": null,
         # "value": description
         # },
         # {
         # "op": "add",
         # "path": "/fields/System.History",
         # # "from": null,
         # "value": f"""Please Look at this  {task.level.name} Bug,
         #            Description: {description},
         #            Complaint id:{task.id},
         #            Created_by:{task.created_by.name} """
         # },
         {
         "op": "add",
         "path": "/fields/System.AssignedTo",
         "value": "msumanth750@outlook.com"
         }
        ]
        # try:
        res = azure_workitem_create(org='msumanth750',project='TestProject',type='Task',data=data,assigned_to=None)
        print(res)
        task.azure = str(res['id'])
        task.save()
        # except Exception as e:
        #     print('azure work item creation Failed',e)
        return task



class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ('__all__')

    def create(self,validated_data):
        comment = TaskComment.objects.create(**validated_data)
        if comment.task.azure:
            id = comment.task.azure
            description = comment.description
            level = comment.level
            data = [
             {
             "op": "add",
             "path": "/fields/System.History",
             # "from": null,
             "value": f"{level}||{description} commented by {comment.created_by.name} @ {comment.created_at} "
             },

            ]
            try:
                res = azure_workitem_update(id=id,data=data,org='msumanth750',project='TestProject')
                print(res)
            except Exception as e:
                print('failed azure work item add comment',e)

        return comment




class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('__all__')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('__all__')

class TaskStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields =('__all__')
