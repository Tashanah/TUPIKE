from django import forms
from . models import Recipe,Ratings

class UserUploadRecipes(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model=Recipe
        fields=['title','food_image','description','link']

    
class RatingsForms(forms.ModelForm):
    

    class Meta:
        model=Ratings
        exclude=['user','recipe']