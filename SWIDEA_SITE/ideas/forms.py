from django import forms
from .models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'image', 'content', 'interest', 'devtools']
        
        widgets = {
            'devtools': forms.SelectMultiple(attrs={
                'style': 'width: 200px; height: 100px;'
            }),
        }