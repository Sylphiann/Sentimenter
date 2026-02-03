from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class DashboardRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',) 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_platform_admin = True

        if commit:
            user.save()
        return user