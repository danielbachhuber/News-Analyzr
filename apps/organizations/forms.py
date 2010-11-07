from django import forms

from apps.organizations.models import *

class OrganizationBasicInfoForm(forms.ModelForm):
    
    class Meta:
        model = Organization
        fields = ['homepage']