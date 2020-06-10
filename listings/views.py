from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .choices import bedroom_choices, price_choices, state_choices
from .models import Listing
from contacts.models import Contact


def index(request):
    listings = Listing.objects.order_by("price").filter(is_published=True)
    paginator = Paginator(listings, 6)
    page_number = request.GET.get('page')
    page_listings = paginator.get_page(page_number)

    context = {
        "listings": page_listings
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    has_contacted = False
    if request.user.is_authenticated:
        has_contacted = Contact.objects.filter(listing_id=listing_id, user_id=request.user.id).exists()

    context = {
        "listing": listing,
        "has_contacted": has_contacted
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    query_listings = Listing.objects.order_by("-list_date")

    if 'keywords' in request.GET:
        keywords = request.GET["keywords"]
        if keywords:
            query_listings = query_listings.filter(description__icontains=keywords)

    if 'city' in request.GET:
        city = request.GET["city"]
        if city:
            query_listings = query_listings.filter(city__iexact=city)

    if 'state' in request.GET:
        state = request.GET["state"]
        if state:
            query_listings = query_listings.filter(state__iexact=state)

    if 'bedrooms' in request.GET:
        bedrooms = request.GET["bedrooms"]
        if bedrooms:
            query_listings = query_listings.filter(bedrooms__gte=bedrooms)

    if 'price' in request.GET:
        price = request.GET["price"]
        if price:
            query_listings = query_listings.filter(price__lte=price)

    context = {
        "bedroom_choices": bedroom_choices,
        "price_choices": price_choices,
        "state_choices": state_choices,
        "listings": query_listings,
        "values": request.GET
    }
    return render(request, 'listings/search.html', context)
