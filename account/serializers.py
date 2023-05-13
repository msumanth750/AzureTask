from rest_framework import serializers
from account.models import User,Profile,Organisation,Project
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from tasks.models import Task
class ProjectSerialiser(serializers.ModelSerializer):
    tasks_reports = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Project
        fields = ('id','name','tasks_reports')

    def get_tasks_reports(self,obj):
        tasks = Task.objects.filter(project=obj)
        reports ={}
        reports['total'] = tasks.count()
        reports['close'] = tasks.filter(status_id=1).count()
        reports['Active'] = tasks.filter(status_id=2).count()
        reports['Pending'] = tasks.filter(status_id=3).count()
        return reports

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'password2', 'tc']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    role_name = serializers.ReadOnlyField(source='role.name')
    type_name = serializers.ReadOnlyField(source='type.name')
    org_name = serializers.ReadOnlyField(source='org.name')
    project = ProjectSerialiser(read_only=True,many=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'name','is_admin',
            'type_name',
            'role_name',
            'org',
            'org_name',
            # 'project',
            'is_verified','project']
    # def get_projects(self,obj):
    #     projects = obj.project.list
    #     print(projects)
    #     return None
class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      # Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')


class OrganisationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('__all__')

class ReportsSerializer(serializers.ModelSerializer):
    tasks_report = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ('id','name','tasks_report')

    def get_tasks_report(self,obj):
        projects = obj.project.all()
        reports = []
        if projects:
            for project in projects:
                tasks = Task.objects.filter(project=project)
                report = {}
                report['project_name'] = project.name
                report['total']=tasks.count()
                report['Open']=tasks.filter(status__name='Open').count()
                report['Todo']=tasks.filter(status__name='Todo').count()
                report['Progress']=tasks.filter(status__name='Progress').count()
                report['Pending']=tasks.filter(status__name='Pending').count()
                report['Close']=tasks.filter(status__name='Close').count()
                report['Critial']=tasks.filter(level__name='Critical').count()
                report['Emergency']=tasks.filter(level__name='Emergency').count()
                report['Bug']=tasks.filter(level__name='Bug').count()
                reports.append(report)
        return reports

class UserlistSerializer(serializers.ModelSerializer):
    role_name = serializers.ReadOnlyField(source='role.name')
    type_name = serializers.ReadOnlyField(source='type.name')
    org_name = serializers.ReadOnlyField(source='org.name')
    projects_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ('id','name',
                  'is_active',
                  'created_at',
                  'updated_at',
                  'org_name',
                  'type_name',
                  'role_name',
                  'is_verified','projects_name')
    def get_projects_name(self,obj):
        projects = obj.project.all()
        names = [p.name for p in projects]
        return ','.join(names)
