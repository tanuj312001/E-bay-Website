from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('createListing',views.createListing,name='createListing'),
    path("<int:listing_id>",views.makeBid,name='makeBid'),
    path("<int:listing_id>/close",views.closeListing,name='closeListing'),
    path("<int:listing_id>/comment",views.comment,name='comment')

]
