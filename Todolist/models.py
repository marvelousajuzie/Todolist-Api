from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.CharField(max_length=250, unique= True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email

class TodoList(models.Model):
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    title = models.CharField(max_length= 300)
    description = models.TextField()
    due_date = models.DateTimeField(auto_now_add= True, blank= True, null= True)
    is_completed = models.BooleanField( default= False)
   

    def __str__(self):
        return self.title

