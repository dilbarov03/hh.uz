from common.models import User
from rest_framework import serializers
from vacancy.models import Category, Vacancy, Company, Worker


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ["username", "full_name"]

class ChildCategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = ['name', 'vacancy_count', 'parent', "min_salary", "max_salary"]

class ParentCategorySerializer(serializers.ModelSerializer):
   child_category = ChildCategorySerializer(many=True)
   class Meta:
      model = Category
      fields = ['name', 'vacancy_count', 'parent', 'min_salary', 'max_salary', "child_category"]

class CompanyRegionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Company
      fields = ['title', 'vacancy_count']   

class CompanyNameSerializer(serializers.ModelSerializer):
   class Meta:
      model = Company
      fields = ['title']

class VacancyRegionSerializer(serializers.ModelSerializer):
   company = CompanyNameSerializer(read_only=True)
   class Meta:
      model = Vacancy
      fields = ['title', 'company', 'min_salary', 'max_salary']

class RegionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = ['name']

class WorkerResumeSerializer(serializers.ModelSerializer):
   class Meta:
      model = Worker
      fields = ['resume']

class WorkerSerializer(serializers.ModelSerializer):
   saved_jobs = VacancyRegionSerializer(many=True)
   applied_jobs = VacancyRegionSerializer(many=True)
   class Meta:
      model = Worker
      fields = "__all__"

class VacancySerializer(serializers.ModelSerializer):
   class Meta:
      model = Vacancy
      fields = "__all__"

class VacancyForCompanySerializer(serializers.ModelSerializer):
   class Meta:
      model = Vacancy
      fields = ['title']

class AppliedUserSerializer(serializers.ModelSerializer):
   applied_jobs = VacancyForCompanySerializer(many=True)
   user = UserSerializer(read_only=True)
   class Meta:
      model = Worker
      fields = ["user","resume", "applied_jobs"]

class CompanySerializer(serializers.ModelSerializer):
   class Meta:
      model = Company
      fields = "__all__"