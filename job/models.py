from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class JobListing(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    image = models.ImageField(
        upload_to="job_images/",
        null=True,
        blank=True
    )
    date_posted = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('title', 'company', 'location')
        
    def __str__(self):
        return f"{self.title} at {self.company} ({self.location})"
    
@receiver(post_delete, sender=JobListing)
def delete_job_logo(sender, instance, **kwargs):
    if instance.image and instance.image.storage.exists(instance.image.name):
        instance.image.delete(save=False)
