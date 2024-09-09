# E-Commerce Auction Site

An eBay-like e-commerce auction site built with Django, allowing users to post auction listings, place bids, comment on those listings, and add listings to a "watchlist."

## Features

- **User Authentication:** Users can register, log in, and log out.
- **Create Listing:** Users can create new auction listings with a title, description, starting bid, optional image URL, and category.
- **Active Listings Page:** Displays all currently active auction listings with details like title, description, current price, and image.
- **Listing Page:** Provides detailed information about a specific auction listing. Signed-in users can:
  - Add or remove items from their "Watchlist."
  - Place a bid, provided it meets the minimum and competitive criteria.
  - Close the auction if they are the listing creator.
  - View the winner if the auction is closed.
  - Add comments to the listing.
- **Watchlist:** Displays all listings a user has added to their watchlist.
- **Categories:** Users can browse all listing categories and view active listings in a selected category.

## How to Use

- **Register:** Create an account to start using the platform.
- **Create a Listing:** Go to the "Create Listing" page and fill in the details.
- **View Active Listings:** Visit the homepage to see all active auctions.
- **Bid on a Listing:** Click on a listing to view details and place a bid.
- **Watchlist:** Add or remove listings from your watchlist.
- **Categories:** Browse and filter listings by category.
- **Close Auction:** If you created the listing, you can close the auction.
