from functools import reduce
import operator
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Min, Max
from vacancy.models import Category, Vacancy, Company, Worker
from django.db.models import Q
from .serializers import *
from rest_framework import status

class CategoryView(generics.ListAPIView):
   queryset = Category.objects.filter(parent=None).all()
   serializer_class = ParentCategorySerializer

class GeneralInfoView(APIView):
   def get(self, request, format=None):
      vacancy_count = Vacancy.objects.all()
      companies_count = Company.objects.all()
      resume_count = Worker.objects.exclude(status__isnull=True).all()

      data = {
         "Vacancies": len(vacancy_count),
         "Companies": len(companies_count),
         "Resumies": len(resume_count)
      }

      return Response(data)

class RegionView(APIView):
   def get(self, request, *args, **kwargs):
      region = self.kwargs.get("region").capitalize()
      companies = Company.objects.filter(company_vacancy__region=region).all()
      comp_serializer = CompanyRegionSerializer(companies, many=True)

      vacancies = Vacancy.objects.filter(region=region).all()
      vac_serializer = VacancyRegionSerializer(vacancies, many=True)

      categories = Category.objects.filter(job_vacancy__region=region).all()
      cat = []
      for category in categories:
         res = {
            "name": category.parent.name
         }
         if res not in cat:
            cat.append(res)

      output = {
         f"Компании в {region}": comp_serializer.data,
         f"Вакансии дня в {region}": vac_serializer.data,
         f"Работа по профессиям в {region}": cat
      }

      return Response(output)

"""     WORKER
TODO
   - /home/worker
   Отклики
   Избранные вакансии
   Рекомендуем лично вам


   - /vacancy/id/apply
   - /upload/resume

"""

class WorkerHomeView(APIView):
   def get(self, request, *args, **kwargs):
      worker = Worker.objects.filter(user=request.user).first()
      recommended_jobs = Vacancy.objects.filter(reduce(operator.or_, (Q(title__contains=word) for word in worker.desired_job_title.split())))
      recJobs_serializer = VacancyRegionSerializer(recommended_jobs, many=True)
      savedJobs_Serializer = VacancyRegionSerializer(worker.saved_jobs, many=True)
      appliedJobs_Serializer = VacancyRegionSerializer(worker.applied_jobs, many=True)

      result = {
         "Избранные вакансии" : savedJobs_Serializer.data, 
         "Отклики": appliedJobs_Serializer.data,
         "Рекомендуем лично вам": recJobs_serializer.data
      }

      return Response(result)

class WorkerGetCreateView(generics.ListCreateAPIView):
   queryset = Worker.objects.all()
   serializer_class = WorkerSerializer

class VacancyApplyView(APIView):
   def post(self, request, *args, **kwargs):
      vacancy = Vacancy.objects.get(pk=self.kwargs.get("pk"))
      worker = Worker.objects.filter(user=request.user).first()
      if vacancy and worker:
         if vacancy not in worker.applied_jobs.all():
            worker.applied_jobs.add(vacancy)
            worker.save()
            appliedJobs_Serializer = VacancyRegionSerializer(worker.applied_jobs, many=True)
            return Response({"status": "You applied successfully to this job", 
            "Your applied vacancies": appliedJobs_Serializer.data})
         return Response({"msg": "You have already applied to this job"})

class AppliedJobsView(APIView):
   def get(self, request):
      worker = Worker.objects.filter(user=request.user).first()
      appliedJobs_Serializer = VacancyRegionSerializer(worker.applied_jobs, many=True)
      return Response(appliedJobs_Serializer.data)

class UpdateResumeView(APIView):
   def get(self, request):
      worker = Worker.objects.filter(user=self.request.user).first()
      resume_serializer = WorkerResumeSerializer(worker)
      return Response(resume_serializer.data)

   def put(self, request):
      worker = Worker.objects.filter(user=self.request.user).first()
      serializer = WorkerResumeSerializer(worker, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUpdateProfileView(APIView):
   def get(self, request):
      worker = Worker.objects.filter(user=self.request.user).first()
      worker_serializer = WorkerSerializer(worker)
      return Response(worker_serializer.data)

   def put(self, request):
      worker = Worker.objects.filter(user=self.request.user).first()
      serializer = WorkerSerializer(worker, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
TODO
   - /company/vacancies - get vacancies or post a new vacancy
   - /vacancy/<id>/applied_users - see who applied to your vacancy
"""

class CompanyListCreateView(generics.ListCreateAPIView):
   queryset = Company.objects.all()
   serializer_class = CompanySerializer

class CompanyVacancyView(generics.ListCreateAPIView):
   serializer_class = VacancySerializer

   def get_queryset(self):
      user = self.request.user
      company = Company.objects.get(user=user)
      return Vacancy.objects.filter(company=company).all()

class AppliedUsersView(generics.ListAPIView):
   serializer_class = AppliedUserSerializer
   
   def get_queryset(self):
      user = self.request.user
      company = Company.objects.get(user=user)
      return Worker.objects.filter(applied_jobs__company=company).all() 


class CompanyGetUpdateView(APIView):
   def get(self, request):
      company = Company.objects.filter(user=self.request.user).first()
      serializer = CompanySerializer(company)
      return Response(serializer.data)

   def put(self, request):
      company = Company.objects.filter(user=self.request.user).first()
      serializer = CompanySerializer(company, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)