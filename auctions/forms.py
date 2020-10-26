from django import forms
from .models import Listing,Bid,Comment
from django.utils import timezone

class ListingForm(forms.ModelForm):
    class Meta:
        model=Listing
        fields=['title','description','category','product_date','startingBid','image']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'startingBid':forms.NumberInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'})
        }

class BidForm(forms.ModelForm):
    class Meta:
        model=Bid
        fields=['offer']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']
        widgets={
            'comment':forms.TextInput(attrs={'class':'form-control',
            'placeholder':' Leave a comment down here'})
        }