from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, UserManager


################# Begin with Model USERS #####################

class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    password = models.CharField(max_length=120)
    verif_password = models.CharField(max_length=120)
    ip_address = models.GenericIPAddressField(protocol="both", unpack_ipv4=False, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects=UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_module_perms(self, app_label):
        return True
    def has_perm(self, perm, obj=None):
        return self.is_admin


class PostingModels(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    img = models.ImageField(upload_to='posting/%Y/%m/%d/', null=True, blank=True)
    title = models.CharField(max_length=256, unique=True, null=True, blank=True)
    desc = models.CharField(max_length=70, null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'Posting'

class CommentModels(models.Model):
    username = models.CharField(max_length=30)
    comment = models.CharField(max_length=150)
    toPost = models.ForeignKey(PostingModels, on_delete=models.CASCADE, to_field='id')
    ip_address = models.GenericIPAddressField(protocol="both")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'Comment'
##################### End with Model USERS #####################