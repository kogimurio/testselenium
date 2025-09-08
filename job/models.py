from django.db import models

class JobListing(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    date_posted = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('title', 'company', 'location')
        
    def __str__(self):
        return f"{self.title} at {self.company} ({self.location})"
