from django import forms
from .models import User

class NewUserForm(forms.ModelForm):
        
    class Meta:
        model = User
        fields = ("username",)

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        
        if commit:
            user.save()
            return user