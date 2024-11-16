from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
# Create your models here.



class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            # Append a unique identifier if the slug already exists
            while Room.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room: {self.name} | ID: {self.slug}"
    


    
    
class Messages(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on =models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return "Message is :- "+ self.content
    