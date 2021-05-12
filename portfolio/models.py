from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    subject = models.CharField(max_length=40)
    message = models.CharField(max_length=450)

    def __str__(self):
        return self.name

