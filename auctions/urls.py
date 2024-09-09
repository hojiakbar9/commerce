from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addToWatchlist/<int:id>", views.addToWatchlist, name="addToWatchlist"),
    path(
        "removeFromWatchlist/<int:id>",
        views.removeFromWatchlist,
        name="removeFromWatchlist",
    ),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_name>", views.category, name="category"),
]
