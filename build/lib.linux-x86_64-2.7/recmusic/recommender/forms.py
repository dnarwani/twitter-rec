from django import forms

class RecommenderForm(forms.Form):
    twitter_handle = forms.CharField(max_length=150)