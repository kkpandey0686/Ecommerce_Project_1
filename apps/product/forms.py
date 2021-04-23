from django import forms
from django.forms import ModelForm
from .models import ProductReview



class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()

class WriteReviewForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ['stars' , 'content']
