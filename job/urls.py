from django.urls import path
from . import views


urlpatterns = [
    path('', views.job_listings, name='job_list'),
    path('add/', views.add_job, name='add_job'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name="delete_job"),
    path('scrape/', views.scrape_linkedin, name="scrape_linkedin"),
]
