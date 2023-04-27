from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self)->str:
        return self.name
    
    class Meta:
        ordering = ['name']
    


class Student(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    def __str__(self)->str:
        return self.name
        
    
class Subject(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self)->str:
        return self.name
    
class Mark(models.Model):
    value = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    