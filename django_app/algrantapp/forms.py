from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }
    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        usernamed = User.objects.filter(username=username)
        if usernamed:
            raise forms.ValidationError("That username is already taken. Please select another")
        emailed = User.objects.filter(email=email)
        if emailed:
            raise forms.ValidationError("An account using that email already exists")
        return cleaned_data

class new_post(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "content",
        ]