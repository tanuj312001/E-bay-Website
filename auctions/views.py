from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ListingForm,BidForm,CommentForm
from .models import User,Listing,Bid,Comment
from django.contrib import messages


def index(request):
    return render(request, "auctions/index.html",{"Listings":Listing.objects.all()})



@login_required
def makeBid(request,listing_id):

    listing=Listing.objects.get(id=listing_id)
    if request.method=='POST':
         form = BidForm(request.POST)
         offer=float(request.POST['offer'])
         if is_validd(offer,listing):
                listing.currentBid = offer
                newBid = form.save(commit=False)
                newBid.listing=listing
                newBid.user = request.user
                newBid.save()
                listing.save()
                

                return HttpResponseRedirect(reverse('makeBid',args=[listing_id]))   
         else:
             messages.success(request, 'bid should be more')

               

             return render(request,"auctions/makeBid.html",{
                 'form':form,
                 'listing':listing,
                 'Comments':listing.all_comments.all(),
                 'commentForm':CommentForm()

             })       

             
    return render(request,'auctions/makeBid.html',{
        'listing':listing,'form':BidForm(),'Comments':listing.all_comments.all(),
                 'commentForm':CommentForm

    })

def closeListing(request,listing_id):
    listing=Listing.objects.get(id=listing_id)
    if request.user==listing.user:
        listing.flActive=False
        listing.save()
        return HttpResponseRedirect(reverse('index'))
 
    
def is_validd(offer,listing):
    if offer>listing.startingBid and (listing.currentBid is None or offer>listing.currentBid):
        return True
    else:
        return False    



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

@login_required
def createListing(request):
    if request.method=="POST":
        form=ListingForm(request.POST,request.FILES)
        if form.is_valid():
            newListing=form.save(commit=False)
            newListing.user=request.user
            newListing.save()
            
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,"auctions/createListing.html",{
                'form': form
            })    
    else:
        return render(request,"auctions/createListing.html",{
            'form':ListingForm()
        })                


@login_required
def comment(request,listing_id):
    listing=Listing.objects.get(id=listing_id)
    
    
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            newComment=form.save(commit=False)
            newComment.user=request.user
            newComment.listing=listing
            listing.save()
        
            newComment.save()
            return HttpResponseRedirect(reverse('makeBid',args=[listing_id]))

    
    

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



