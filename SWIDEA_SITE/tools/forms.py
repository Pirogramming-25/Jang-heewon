from django.db import models
from django import forms
from .models import DevTool

class DevToolForm(forms.ModelForm):
    class Meta:
        model = DevTool 
        fields = ['name','kind','content']