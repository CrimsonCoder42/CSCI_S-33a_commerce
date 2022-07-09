from django.forms import ModelForm, TextInput, Select, Textarea
from .models import *
# use form models to create all remaining forms
# https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/


class newAuctionListing(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['itemTitle', 'image', 'itemDescription', 'initial_bid', 'auctionCategory']
        # use widgets to add class attribute https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/
        # TextInput for text Select for dropdown
        widgets = {
            'itemTitle': TextInput(attrs={'class': "form-control"}),
            'itemDescription': TextInput(attrs={'class': "form-control"}),
            'initial_bid': TextInput(attrs={'class': "form-control"}),
            'auctionCategory': Select(choices=Category.objects.all(), attrs={'class': "form-control"}),
            }


class newAuctionBid(ModelForm):
    class Meta:
        model = AuctionBid
        fields = ['bid']
        widgets = {
            'bid': TextInput(attrs={'class': "form-control"})
            }


class newComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'class': "form-control", 'cols': 80, 'rows': 20})
            }