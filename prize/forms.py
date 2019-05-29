from django import forms
from . models import Projects,Ratings

class UserUploadProjects(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model=Projects
        fields=['title','image_landing','description','link']

    
class RatingsForms(forms.ModelForm):
    

    class Meta:
        model=Ratings
        exclude=['user','project']