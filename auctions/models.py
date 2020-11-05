from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    image = models.URLField()
    content = models.TextField(max_length=512)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    winner = models.CharField(max_length=128)

    def __str__(self):
        return f"Listing {self.id} : {self.title} published on {self.date} by {self.seller}. Starting bid : ${self.starting_bid} - Category : {self.category} "


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid for auction number {self.auction.id} : {self.auction.title} of ${self.amount} made by {self.user} on {self.date}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.listing.title} : {self.comment}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Watchlist of user {self.user}"
