from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username,tc, password=None,password2=None,profile_picture=None,):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            tc=tc,
        )     
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username,tc, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username=models.CharField(max_length=200)
    tc=models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to=upload_to,default='media/1658384701097-01.jpeg',blank=True,null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username","tc",'profile_picture']

    def __str__(self):
        return self.email

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