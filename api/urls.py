from django.urls import include, path
from .views import *

urlpatterns = [
   #general 
   path("general/", GeneralInfoView.as_view()),
   path("category/", CategoryView.as_view()),
   path("region/<str:region>/", RegionView.as_view()),

   #worker
   path("home/worker", WorkerHomeView.as_view()),
   path("worker/", WorkerGetCreateView.as_view()),
   path("vacancy/<int:pk>/apply", VacancyApplyView.as_view()),
   path("worker/applied_jobs", AppliedJobsView.as_view()),
   path("worker/resume", UpdateResumeView.as_view()),
   path("worker/profile", GetUpdateProfileView.as_view()),

   #company
   path("company/", CompanyListCreateView.as_view()),
   path("company/vacancy", CompanyVacancyView.as_view()),
   path("company/applied_users/", AppliedUsersView.as_view()),
   path("company/update", CompanyGetUpdateView.as_view()),
]