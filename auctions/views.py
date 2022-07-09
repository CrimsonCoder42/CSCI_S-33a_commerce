from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .forms import *
from .models import User, Category, AuctionWatchList, AuctionListing, AuctionBid, Comment


# modify index to get all active items.
def index(request):
    # if not signed in display all items by itemActive only
    auction_listing = AuctionListing.objects.filter(itemActive=True)
    current_user = request.user
    if not request.user.is_authenticated:
        return render(request, "auctions/index.html", {
            'auction_listing': auction_listing
        })
    else:
        auctionwatchlist = AuctionWatchList.objects.get(user=current_user)
        userbid = AuctionBid.objects.get(itemCreator=current_user)
        created_items = AuctionListing.objects.get(itemCreator=current_user)

        return render(request, "auctions/index.html", {
            'auction_listing': auction_listing,
            'auctionwatchlist': auctionwatchlist,
            'userbid': userbid,
            'created_items': created_items
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# use .is_authenticated to validate if user is signed in and
# registered https://docs.djangoproject.com/en/4.0/topics/auth/default/
def user_listing(request, user):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        # use .objects .filter() and .get() for user name and
        # to extract Auctionand wacthlist https://docs.djangoproject.com/en/4.0/ref/models/querysets/
        user_name = User.objects.get(username=user)
        user_watchlist = AuctionListing.objects.filter(user=user_name)
        auction_items = AuctionListing.objects.filter(user=user_name)

        return render(request, "auctions/user_listings", {
            "user_watchlist": user_watchlist,
            "auction_items": auction_items
        })


# creating a new auction item
def create_newAuctionListing(request):
# if user is authenticated continue if not go to log in

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

# if it's a POST take in the data information and redirect

    if request.method == "POST":
        new_form = newAuctionListing(request.POST, request.FILES)

        if new_form.is_valid():

            # clean and normalize the data for consistant format
            itemTitle = new_form.cleaned_data['itemTitle']
            image = new_form.cleaned_data['image']
            itemDescription = new_form.cleaned_data['itemDescription']
            initial_bid = new_form.cleaned_data['initial_bid']
            auctionCategory = new_form.cleaned_data['auctionCategory']

# using .save with the model https://docs.djangoproject.com/en/4.0/ref/models/instances/

            auc_listing = AuctionListing(
                itemTitle=itemTitle,
                image=image,
                itemDescription=itemDescription,
                initial_bid=initial_bid,
                auctionCategory=auctionCategory
            )
            auc_listing.save()

# route back to users current listing

            return redirect('user_listing')

# if not a POST generate a from to be filled out for new auction item

    else:
        return render(request, "auctions.create_listing.html", {
            'form': newAuctionListing()
        })




