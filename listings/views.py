from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .choices import price_choices, bedroom_choices, state_choices
from .models import Listing


# Create your views here.
def index(request):
    listings = Listing.objects.order_by("-list_date").filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get("page")
    paged_listings = paginator.get_page(page)

    context = {
        "listings": paged_listings
    }

    return render(request, "listings/listings.html", context) 

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        "listing": listing
    }

    return render(request, "listings/listing.html", context) 

def search(request):
    queryset_list = Listing.objects.order_by("-list_date")

    # Keywords
    if "keywords" in request.POST:
        keywords = request.POST["keywords"]
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    
    # City
    if "city" in request.POST:
        city = request.POST["city"]
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if "state" in request.POST:
        state = request.POST["state"]
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if "bedrooms" in request.POST:
        bedrooms = request.POST["bedrooms"]
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if "price" in request.POST:
        price = request.POST["price"]
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        "state_choices": state_choices,
        "bedroom_choices": bedroom_choices,
        "price_choices": price_choices,
        "listings": queryset_list,
        "values": request.POST,
    }

    return render(request, "listings/search.html", context) 
