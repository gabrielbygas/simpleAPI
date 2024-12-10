from django.db import models
from django.urls import reverse
# Create your models here.

class Persons(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse("simpleapi:person_api_view_detail", kwargs={"pk": self.pk})
    
    def get_age_in_years(self):
        return f'{self.age} ans'
    
    def __str__(self):
        return self.firstname + " " + self.lastname