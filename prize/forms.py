from django import forms
from . models import Projects

class UserUploadProjects(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model=Projects
        fields=['project','project']