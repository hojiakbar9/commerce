from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max

class ListingForm(forms.Form):
    CATEGORIES = [(" ", "")] + list(Category.objects.all().values_list())

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "label": "Title",
                "max_length": "100",
                "required": "True",
                "class": "form-control",
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "5",
                "cols": "50",
                "class": "form-control",
            }
        ),
        required=True,
    )
    price = forms.FloatField(
        widget=forms.NumberInput(attrs={"min": "0", "class": "form-control"}),
        required=True,
    )
    image = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    category = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )

def index(request):
    return render(
        request,
        "auctions/index.html",
        {"listings": AuctionListings.objects.filter(isActive=True).all()},
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = float(form.cleaned_data["price"])
            image_url = form.cleaned_data["image"]

            category_name = form.cleaned_data["category"]
            if category_name == " ":
                category = Category.objects.get(category_name="Other")
            else:
                category = Category.objects.get(pk=category_name)
            AuctionListings(
                title=title,
                description=description,
                image=image_url,
                price = price,
                owner=request.user,
                category=category,
            ).save()
            messages.success(request, "Successfully created listing!")
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {"form": ListingForm()})


def listing(request, id):
    listing = AuctionListings.objects.get(pk=id)
    isInWatchlist = request.user in listing.watchlist.all()
    
    bids= Bids.objects.filter(listing=listing)
    
    if bids.exists:
        heighestBid = bids.aggregate(Max('bid'))['bid__max']
        if heighestBid:
            highestBidder = bids.filter(bid=heighestBid).first().user
        else:
            highestBidder =None
    else:
        highestBidder=None
    numberOfBids = bids.all().count() 
    

    try:
        comments = Comments.objects.filter(listing=listing).all()
    except Comments.DoesNotExist:
        comments = None
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "isInWatchlist": isInWatchlist,
            "comments": comments,
            "numberOfBids" : numberOfBids,
            "bidOwner": highestBidder
        },
    )


@login_required
def addToWatchlist(request, id):
    listing = AuctionListings.objects.get(pk=id)
    listing.watchlist.add(request.user)
    messages.success(request, "Added to Watchlist!")
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def removeFromWatchlist(request, id):
    listing = AuctionListings.objects.get(pk=id)
    listing.watchlist.remove(request.user)
    messages.info(request, "Removed From Watchlist")
    return HttpResponseRedirect(reverse("listing", args=(id,)))

@login_required
def bid(request, id):
    listing = AuctionListings.objects.get(pk=id)
    current_price = listing.price

    if request.method == "POST":
        offered_bid = float(request.POST["bid"])

        if offered_bid > current_price:
            bid = Bids(bid=offered_bid, user=request.user, listing = listing)
            bid.save()
            listing.price = offered_bid
           

            # Add the listing to the watchlist if not so done
            if request.user not in listing.watchlist.all():
                listing.watchlist.add(request.user)
                messages.info(request, "Added to Watchlist!")

            listing.save()
        
            messages.success(request, "Successfully placed bid!")    
            return HttpResponseRedirect(reverse("listing", args=(id,)))
        else:
            messages.error(request, "Offered bid is lower than the current price!")
            return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def closeAuction(request, id):
    listing = AuctionListings.objects.get(pk=id)
    listing.isActive = False
    listing.save()
    messages.info(request, 'The listing was closed!')
    return HttpResponseRedirect(reverse("index"))


def watchlist(request):
    return render(
        request,
        "auctions/watchlist.html",
        {"watchlist": AuctionListings.objects.filter(watchlist=request.user).all()},
    )


@login_required
def comment(request, id):
    listing = AuctionListings.objects.get(pk=id)
    comment = Comments( content=request.POST["content"], author=request.user, listing=listing)
    comment.save()        
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def categories(request):
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": Category.objects.all()
            .distinct()
            .order_by("category_name")
            
        },
    )


def category(request, category_name):
    category = Category.objects.get(category_name=category_name)

    return render(
        request,
        "auctions/category.html",
        {"listings": category.listings.all()},
    )
