from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ForumPost, Comment, Profile


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        profile = Profile(user=user)
        profile.bio = "empty bio"
        if commit:
            user.save()
            profile.save()
        return user


class RatingForm(forms.Form):
    user_rating = forms.CharField(label="Your grade", max_length=1)


class CreateInForumPost(ModelForm):
    class Meta:
        model = ForumPost
        fields = "__all__"


class CreateInComment(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {"name": forms.HiddenInput(), "email": forms.HiddenInput()}


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control-file"})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5})
    )

    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
