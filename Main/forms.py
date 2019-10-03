from django import forms

from django.shortcuts import redirect
from django.shortcuts import reverse

from django.contrib.auth import authenticate
from django.contrib.auth import login


from .models import MyArticles
from .models import Tag

from django.contrib.auth.models import User

#create your forms here.
class ArticleForm(forms.ModelForm):
    class Meta:
        model = MyArticles
        fields = [
            'name',
            'text',
            'color',
            'tag',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control'}),
            'tag':  forms.Select(attrs={'class':'form-control'}),
            'color':  forms.Select(attrs={'class':'form-control'}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}) ,
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            '_password': forms.PasswordInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }
class LoginUserForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        label="Имя пользователя",
        widget=forms.TextInput,
        )
    username.widget.attrs.update({
        'class': 'form-control',
    })
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
    )
    password.widget.attrs.update({
        'class':'form-control'
    })
    def clean_username(self):
        list_users = User.objects.filter(
            username=self.cleaned_data['username'],
        )
        if len(list_users) < 1:
            raise forms.ValidationError(
            ("Нет %(name)s пользователя"),
            params={'name': self.cleaned_data['username']},
        )

