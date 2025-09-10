from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import JobListing
from django.http import HttpResponse
from datetime import date


def job_listings(request):
    jobs = JobListing.objects.all().order_by('-date_posted')
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'jobs/job_list.html', {'page_obj': page_obj})


def scrape_and_save(job_data):
    # Example uniqueness rule: title, compant, location
    job, created = JobListing.objects.get_or_create(
        title = job_data['title'],
        company = job_data['company'],
        location = job_data['location'],
        defaults={'url': job_data['url'], 'date_posted': job_data['date_posted']}
    )
    return created


def add_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        url = request.POST.get('url')
        
        try:
            job, created = JobListing.objects.get_or_create(
                title=title,
                company=company,
                location=location,
                defaults={'url': url, 'date_posted': date.today()}
            )
            if created:
                return redirect('/')
            else:
                return HttpResponse("Job already exists.")
        except Exception as e:
            return HttpResponse(f"Error same url already exists")
    return render(request, 'jobs/add_job.html')

def edit_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company = request.POST.get('company')
        job.location = request.POST.get('location')
        job.url = request.POST.get('url')
        job.save()
        return redirect("job_list")
        
    return render(request, 'jobs/edit_job.html', {'job': job})


def delete_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    job.delete()
    return redirect('job_list')

