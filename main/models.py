from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text
    
class ScheduleItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.CharField(max_length=200)
    date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.activity} at {self.start_time}"