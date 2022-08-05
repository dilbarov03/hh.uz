from django.db import models
from django.template.defaultfilters import truncatechars
from common.models import User
from helpers.models import BaseModel, generate_unique_slug

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


class Company(BaseModel):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   title = models.CharField(max_length=128)
   slug = models.CharField(max_length=256, blank=True, null=True)
   description = models.TextField(null=True, blank=True)
   vacancy_count = models.IntegerField(default=0)
   location = models.CharField(max_length=128, null=True, blank=True)

   def __str__(self):
      return self.title

   def save(self, *args, **kwargs):
      if hasattr(self, "slug") and hasattr(self, "title"):
         if not self.slug:
               self.slug = generate_unique_slug(self.__class__, self.title)

      super().save(*args, **kwargs)

   @property
   def short_description(self):
      return truncatechars(self.description, 35)

class Category(BaseModel):
   name = models.CharField(max_length=128)
   slug = models.CharField(max_length=256, blank=True, null=True)
   vacancy_count = models.IntegerField(default=0)
   min_salary = models.IntegerField(default=9999999999)
   max_salary = models.IntegerField(default=0)
   parent = models.ForeignKey("self", null=True, blank=True, 
               related_name="child_category", on_delete=models.CASCADE)
   
   def __str__(self):
      return self.name

   def save(self, *args, **kwargs):
      if hasattr(self, "slug") and hasattr(self, "name"):
         if not self.slug:
               self.slug = generate_unique_slug(self.__class__, self.name)
      super().save(*args, **kwargs)

class Vacancy(BaseModel):
   title = models.CharField(max_length=128)
   slug = models.CharField(max_length=256, blank=True, null=True)
   description = models.TextField()
   company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_vacancy")
   job = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="job_vacancy")
   min_salary = models.BigIntegerField(null=True, blank=True)
   max_salary = models.BigIntegerField(null=True, blank=True)
   is_active = models.BooleanField(default=True)
   is_remote = models.BooleanField(default=False)
   region = models.CharField(max_length=128, null=True, blank=True, choices=REGION_CHOICES)

   def __str__(self):
      return self.title


   @property
   def short_description(self):
      return truncatechars(self.description, 35)

   def save(self, *args, **kwargs):
      if hasattr(self, "slug") and hasattr(self, "title"):
         if not self.slug:
               self.slug = generate_unique_slug(self.__class__, self.title)
      company = self.company
      company.vacancy_count+=1
      company.save()
      category = self.job
      category.vacancy_count+=1
      if self.min_salary<category.min_salary:
         category.min_salary = self.min_salary
      if self.max_salary>category.max_salary:
         category.min_salary = self.min_salary
      
      parent = category.parent
      
      if parent:
         parent.vacancy_count+=1

         if self.min_salary<parent.min_salary:
            parent.min_salary = self.min_salary
         if self.max_salary>parent.max_salary:
            parent.min_salary = self.min_salary

         parent.save()
      category.save()
      
      

      super().save(*args, **kwargs)

class Worker(BaseModel):
   WORKER_STATUS = (
      ('active', 'active'), #Is actively looking for a job
      ('open', 'open'), #Is open for offers
      ('closed', 'closed') #Is not looking for a job
   )
   
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   description = models.TextField(null=True, blank=True)
   desired_job_title = models.CharField(max_length=128,null=True, blank=True)
   resume = models.FileField(upload_to="files/", blank=True, null=True)
   status = models.CharField(max_length=128, choices=WORKER_STATUS)
   saved_jobs = models.ManyToManyField(Vacancy, blank=True)
   applied_jobs = models.ManyToManyField(Vacancy, blank=True, related_name="applied_users")
   region = models.CharField(max_length=128, choices=REGION_CHOICES)

   def __str__(self):
      return self.user.full_name

   @property
   def short_description(self):
      return truncatechars(self.description, 35)


   def save(self, *args, **kwargs):
      if hasattr(self, "slug") and hasattr(self, self.user.full_name):
         if not self.slug:
               self.slug = generate_unique_slug(self.__class__, self.user.full_name)

      if hasattr(self, "slug") and hasattr(self, self.user.username):
         if not self.slug:
               self.slug = generate_unique_slug(self.__class__, self.user.username)
               

      super().save(*args, **kwargs)