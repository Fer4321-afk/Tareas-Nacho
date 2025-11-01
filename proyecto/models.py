from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)
    birth = models.DateField()
    slug = models.SlugField()

    def __str__(self):
        return self.name
