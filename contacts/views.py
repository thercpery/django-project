from django.shortcuts import render, redirect
from django.contrib import messages
from mailjet_rest import Client
from .models import Contact
from dotenv import load_dotenv
import os
load_dotenv(".env")



# Create your views here.
def contact(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = request.POST["listing"]
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]
        user_id = request.POST["user_id"]
        realtor_email = request.POST["realtor_email"]
        realtor_name = request.POST["realtor_name"]

        # Check if user has made an inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, "You have already made an inquiry for this listing.")
                return redirect(f"/listings/{listing_id}")
                

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        # Send email
        mailjet = Client(auth=(os.environ.get("MAILJET_API_KEY"), os.environ.get("MAILJET_API_SECRET")), version='v3.1')
        data = {
        'Messages': [
            {
            "From": {
                "Email": "sarsicoola@gmail.com",
                "Name": "BT Real Estate"
            },
            "To": [
                {
                    "Email": realtor_email,
                    "Name": realtor_name
                },
                {
                    "Email": "thercpery@gmail.com",
                    "Name": "BT Admin"
                }
            ],
            "Subject": "Property Listing Inquiry",
            "HTMLPart": f"There has been an inquiry for {listing}. Sign into the admin panel for more info.",
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        mailjet.send.create(data=data)

        messages.success(request, "Your request has been submitted, a realtor will get back to you soon.")
        return redirect(f"/listings/{listing_id}")
