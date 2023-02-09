from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
import uuid
class User(AbstractBaseUser):
    uuid=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(null=False, blank=False ,unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def get_short_name(self):
        # The user is identified by their email
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
           return True
    
    def __str__(self):
        return self.email




