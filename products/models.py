from django.db import models
from django.contrib.auth.models import User

CATEGORIAS =[
    ('1', 'Espadaa'),
    ('2', 'Baston'),
    ('3', 'Arco'),
]

class Product(models.Model):
 name = models.CharField(max_length=100)
 price = models.FloatField()
 description = models.TextField()
 category = models.CharField(max_length=3, choices=CATEGORIAS)
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 date_published = models.DateTimeField(auto_now_add=True)

 def __str__(self):
     return  "f{self.name}, by {self.user}" 
# Create your models here.
