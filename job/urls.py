from django.urls import path
from . import views


urlpatterns = [
    path('', views.job_listings, name='home'),
    path('add/', views.add_job, name='add_job'),
]
