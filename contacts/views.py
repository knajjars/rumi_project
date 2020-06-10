from django.shortcuts import redirect
from django.contrib import messages
# from django.core.mail import send_mail

from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contact = Contact.objects.filter(listing_id=listing_id, user_id=user_id).exists()
            if has_contact:
                messages.error(request, "Inquiry pending")
                return redirect('/listings/' + listing_id)

        new_contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone,
                              message=message,
                              user_id=user_id, realtor_email=realtor_email)

        new_contact.save()

        # send_mail("Property Listing Inquiry",
        #           "There has been an Inquiry for: " + listing + ". Check admin panel for more info.",
        #           "", [''], fail_silently=False
        #           )

        messages.success(request, "Inquiry sent!")
        return redirect('/listings/' + listing_id)
