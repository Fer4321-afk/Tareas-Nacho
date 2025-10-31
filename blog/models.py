from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    birth = models.DateField()
    slug = models.SlugField(unique=True)
    propic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Dni(models.Model):
    dni = models.CharField(max_length=10)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, )

    def __str__(self):
        return self.dni
        
class User (models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)


    def __str__(self):
        return self.username 
    
