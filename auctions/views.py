from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib import messages

from .models import *


def index(request):
    listings = Listing.objects.all().filter(active=True)

    return render(request, "auctions/index.html", {
        "listings": listings
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


@login_required(login_url='/login')
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")

    seller = request.user
    title = request.POST.get("title")
    image = request.POST.get("image")

    if image == "":
        image = "https://i.imgur.com/GQPN5Q9.jpg"
    content = request.POST.get("content")
    starting_bid = request.POST.get("starting_bid")

    if starting_bid == "":
        starting_bid = 0

    category = request.POST.get("category")

    new_listing = Listing(seller=seller, title=title, image=image, content=content, starting_bid=starting_bid,
                          current_bid=starting_bid, category=category)
    new_listing.save()
    messages.add_message(request, messages.SUCCESS, "Listing created")
    return HttpResponseRedirect(reverse("view", args=(new_listing.pk,)))


def view(request, pid):
    listing = Listing.objects.get(pk=pid)
    print("pid", pid)
    comments = Comment.objects.filter(listing=listing)
    bids = Bid.objects.filter(listing=listing)

    if request.method == "POST":
        listing = Listing.objects.get(pk=pid)
        bid = float(request.POST.get('bid'))
        if listing.current_bid >= bid:
            messages.add_message(request, messages.ERROR, "Your bid needs to be higher than the current bid")
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "bids": bids,
            })

        user = request.user
        new_bid = Bid(user=user, listing_id=pid, amount=bid)
        new_bid.save()
        listing.current_bid = bid
        listing.save()
        messages.add_message(request, messages.SUCCESS, "Bid added")
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "bids": bids,
        })

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "bids": bids,
    })


def watchlist(request):
    user = request.user
    list_ids = Watchlist.objects.values_list('listing', flat=True).filter(user=user)
    lists = []
    for pid in list_ids:
        lists.append(Listing.objects.get(pk=pid))

    return render(request, "auctions/watchlist.html", {
        "listings": lists
    })


def categories(request):
    return None


def comment(request, pid):
    user = request.user
    cmt = request.POST.get("comment")
    new_comment = Comment(user=user, listing_id=pid, comment=cmt)
    new_comment.save()
    messages.add_message(request, messages.SUCCESS, "Comment added")
    return HttpResponseRedirect(reverse("view", args=(pid,)))


def addwatchlist(request, pid):
    user = request.user
    listing = Listing.objects.get(pk=pid)
    check = Watchlist.objects.filter(user=user, listing_id=pid).first()
    if check is not None:
        messages.add_message(request, messages.ERROR, "Listing already exists in Watchlist")
        return HttpResponseRedirect(reverse("view", args=(pid,)))

    new_watchlist = Watchlist(user=user, listing_id=listing.pk)
    new_watchlist.save()
    messages.add_message(request, messages.SUCCESS, "Added to Watchlist")

    return HttpResponseRedirect(reverse("view", args=(pid,)))


def deletewatchlist(request, pid):
    watch_list = Watchlist.objects.get(listing_id=pid)
    watch_list.delete()
    messages.add_message(request, messages.SUCCESS, 'Listing removed from Watchlist')
    return HttpResponseRedirect(reverse("watchlist"))


def close(request, pid):
    if request.method == "POST":
        listing = Listing.objects.get(pk=pid)
        if request.user == listing.seller:
            listing.active = False

            closed_listing = Bid.objects.filter(listing_id=pid).order_by('-amount').first()

            if closed_listing is None:
                listing.winner = request.user.username
            else:
                listing.winner = closed_listing.user.username

            listing.save()
            messages.add_message(request, messages.SUCCESS, "Listing closed")
            return HttpResponseRedirect(reverse("view", args=(pid,)))
        else:
            messages.add_message(request, messages.ERROR, "You can't close this listing")
            return HttpResponseRedirect(reverse("view", args=(pid,)))


def categories(request):
    listings = Listing.objects.all()
    category_list = []

    for listing in listings:
        if listing.category not in category_list and listing.category != "":
            category_list.append(listing.category)

    return render(request, "auctions/categories.html", {
        "categories": category_list
    })


def get_category(request, category):
    listings = Listing.objects.all()
    list = []
    for l in listings:
        if l.category == category and l.active:
            list.append(l)

    return render(request, "auctions/index.html", {
        "listings": list
    })
