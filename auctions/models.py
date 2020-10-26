from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings




class User(AbstractUser):
    pass

class Category(models.Model):
    pass


class Listing(models.Model):
    product_categories=(
    ('Toy', "Toy"),
    ('Sports', "Sports"),
    ('Fashion', "Fashion"),
    ('Electronics', "Electronics"),
    ('Home', "Home"))

    title=models.CharField(max_length=24)
    flActive=models.BooleanField(default=True)
    description=models.CharField(max_length=900)
    category=models.CharField(max_length=34,choices=product_categories,default='Toy')
    product_date=models.DateField(default=timezone.now())
    startingBid=models.FloatField()
    currentBid = models.FloatField(blank=True,null=True)
    image=models.ImageField(upload_to='auctions/images',default='')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
   

    def __str__(self):
        return f"{self.title} - {self.startingBid} by {self.user}"


class Bid(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='all_userbids')
    offer=models.FloatField()
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='all_bids')


class Comment(models.Model):
    comment=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='all_comments')

    






 

