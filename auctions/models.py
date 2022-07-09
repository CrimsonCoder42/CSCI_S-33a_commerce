from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


# category model groups the listings
class Category(models.Model):
    categoryName = models.CharField(max_length=40)

    def __str__(self):
        return self.categoryName


class AuctionWatchList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='watchlist_for_user')
    currentAuctions = models.ManyToManyField('AuctionListing', related_name='watchlist_auctions', blank=True)


# Use float instead of integer for bids down to the penny
class AuctionListing(models.Model):
    itemTitle = models.CharField(max_length=80)
    itemActive = models.BooleanField(default=True)
    itemImage = models.ImageField(upload_to='images', blank=True,  null=True)
    itemDescription = models.TextField()
    itemCreator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_maker')
    # related_name = 'auction_category'
    auctionCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    initial_bid = models.FloatField()
    current_bid = models.FloatField(blank=True, null=True)
    bid_winner = models.ForeignKey(User, null=True, on_delete=models.PROTECT)

# double check strftime('%B %d %Y') pycharm giving unresolved

    def created_date(self):
        return f"{self.date}"

    def __str__(self):
        return self.itemTitle


class AuctionBid(models.Model):
    itemCreator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_maker_item')
    auctionItem = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_bid_item")
    date = models.DateTimeField(default=timezone.now)
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bid}"

class Comment(models.Model):
    date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')

    def __str__(self):
        return f"{self.user} - {self.date}"