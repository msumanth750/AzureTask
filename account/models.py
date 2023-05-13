from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

#  Custom User Manager
class UserType(models.Model):
    name = models.CharField(max_length=150 ,unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    name=models.CharField(max_length=150 ,unique=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  org = models.ForeignKey('Organisation',on_delete=models.CASCADE,null=True)
  project = models.ManyToManyField('Project',blank=True)
  type = models.ForeignKey('UserType',on_delete=models.CASCADE,null=True)
  role = models.ForeignKey('UserRole',on_delete=models.CASCADE,null=True)
  is_verified = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return f'{self.email}-{self.name}'

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin

genderchoices=[('Female','Female'),
                ('Male','Male'),
                ('Others','Others'),
                ('NA','NA')]

class Profile(models.Model):
    user = models.OneToOneField('User',on_delete=models.CASCADE)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150,null=True)
    phone = models.CharField(max_length=12)
    gender = models.CharField(max_length=10 , choices = genderchoices)
    def __str__(self):
        return self.firstname


class Timestampmodel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Organisation(Timestampmodel):
    name = models.CharField(max_length=100,unique=True)
    type = models.CharField(max_length=56,null=True)

    def __str__(self):
        return self.name

class Project(Timestampmodel):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class ProjectMeta(Timestampmodel):
    project_id = models.ForeignKey('Project',on_delete=models.CASCADE)
    manager = models.ForeignKey('User',on_delete=models.CASCADE,related_name='manager')
    manager2 = models.ForeignKey('User',on_delete=models.CASCADE,related_name='second_manager')
    size = models.IntegerField(default=0)
