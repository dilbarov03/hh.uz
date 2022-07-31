from django.db import models
from common.models import User
from helpers.models import BaseModel, generate_unique_slug


class Company(BaseModel):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   title = models.CharField(max_length=128)
   description = models.TextField(null=True, blank=True)
   vacancy_count = models.IntegerField(default=0)
   location = models.CharField(max_length=128, null=True, blank=True)
   

class Job(BaseModel):
   name = models.CharField(max_length=128)
   slug = models.CharField(max_length=256)
   vacancy_count = models.IntegerField(default=0)
   parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
   

class Vacancy(BaseModel):
   REGION_CHOICES = (
      ('Toshkent', 'Toshkent'),
      ("Farg'ona", "Farg'ona"), 
      ('Andijon', 'Andijon'),
      ('Samarqand', 'Samarqand'),
      ("Buxoro", "Buxoro"),
      ("Navoiy", "Navoiy"),
      ("Qarshi", "Qarshi"),
      ("Nukus", "Nukus"),
      ("Xorazm", "Xorazm"), 
   )

   title = models.CharField(max_length=128)
   slug = models.CharField(max_length=256)
   description = models.TextField()
   company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_vacancy")
   job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_vacancy")
   min_salary = models.BigIntegerField(null=True, blank=True)
   max_salary = models.BigIntegerField(null=True, blank=True)
   is_active = models.BooleanField(default=True)
   is_remote = models.BooleanField(default=False)
   region = models.CharField(max_length=128, null=True, blank=True, choices=REGION_CHOICES)


class Worker(BaseModel):
   WORKER_STATUS = (
      ('active', 'active'), #Is actively looking for a job
      ('open', 'open'), #Is open for offers
      ('closed', 'closed') #Is not looking for a job
   )
   
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   description = models.TextField(null=True, blank=True)
   desired_job_title = models.CharField(null=True, blank=True)
   resume = models.FileField(upload_to="files/", blank=True, null=True)
   status = models.CharField(max_length=128, choices=WORKER_STATUS)
   saved_jobs = models.ManyToManyField(Vacancy, blank=True, null=True)
   applied_jobs = models.ManyToManyField(Vacancy,related_name="applied_users", null=True, blank=True)