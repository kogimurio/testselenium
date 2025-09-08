from django.contrib import admin
from .models import JobListing

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'date_posted')  # fields shown in the list view
    search_fields = ('title', 'company', 'location')  # adds search bar
    list_filter = ('company', 'location', 'date_posted')  # adds filters on the right
