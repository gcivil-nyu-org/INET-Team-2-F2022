from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ForumPost, Comment


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
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
