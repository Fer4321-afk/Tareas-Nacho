from django.contrib import admin
from .models import Person, Dni,User 
 # Auto llenar el campo slug basado en el campo name
   
admin.site.register(Person),
admin.site.register(Dni),
admin.site.register(User),
# Register your models here.
