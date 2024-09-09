from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.category_name


class AuctionListings(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="listings",
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owners")

    watchlist = models.ManyToManyField(
        User, related_name="watchlist_items", blank=True, null=True
    )
    price = models.FloatField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=350)
    isActive = models.BooleanField(default=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    content = models.CharField(max_length=500, default="Hello")

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="all_comments"
    )
    listing = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"Content: {self.content}"


class Bids(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="made_bids", blank=True, null=True
    )
    listing = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name="all_bids"
    )

    def __str__(self):
        return str(self.bid)
