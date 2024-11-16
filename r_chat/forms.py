# forms.py
from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'slug']
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Room.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug is already taken. Please choose a different one.")
        return slug
