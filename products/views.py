from datetime import datetime, timezone
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests

from RentShot import settings

from .models import Product, Availability, Reservation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .forms import ReservationForm , ProductForm
from django import forms
from django.db.models import Q

def singleproduct(request,id):
    product = Product.objects.get(id=id)
    availabilities = Availability.objects.filter(product=product)
    reserve_form = ReservationForm(initial={'product_id': id})
    context = {
        'product': product,
        'availabilities': availabilities,
        'reserve_form' : reserve_form,
    }
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        form.fields["product_id"] = forms.IntegerField(widget=forms.HiddenInput(), initial=id)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            # Check for overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
            product=product,
            start_date__range=[start_date, end_date] | Q(end_date__range=[start_date, end_date]) | Q(start_date__lte=start_date, end_date__gte=end_date)
            )
            if overlapping_reservations.exists():
                messages.error(request, 'Selected dates are not available for this product.')
            else:
                # Calculate total price based on the number of days
                total_price = (end_date - start_date).days * product.price_per_day

                # Create a reservation
                reservation = Reservation(
                    user=request.user,
                    product=product,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=total_price
                )
                reservation.save()

                messages.success(request, 'Reservation successful!')
                return redirect('product_list')
        else:
            messages.error(request, 'Invalid reservation input. Please check the selected dates.')


    return render(request, 'singleproduct.html',context)

def rules(request):
    products = Product.objects.all()

    return render(request, 'rules.html',)

def ticket(request):
    products = Product.objects.all()

    return render(request, 'ticket.html',)

def pro_status(request):
    products = Product.objects.all()

    return render(request, 'pro_status.html',)

def profile_contact(request):
    products = Product.objects.all()

    return render(request, 'profile_contact.html',)

def plans(request):
    products = Product.objects.all()

    return render(request, 'plans.html',)

def product_list(request):
    products = Product.objects.all()
    context = {'product_list' : products}  
    return render(request, 'product_list.html',context)

@login_required
def profile(request):
    products = Product.objects.all()
    context = {'profile' : products}  
    return render(request, 'profile.html',context)

@login_required
def admin_panel(request):
    products = Product.objects.all()

    context = {'product_list' : products}   

    product_form = ProductForm()
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            # Save the form data to create a new Product instance
            new_product = product_form.save(commit=False)
            
            # Set additional fields (e.g., created_at, owner)
            new_product.created_at = datetime.now()
            new_product.owner = request.user

            # Save the Product instance
            new_product.save()

            # Redirect to a success page or do something else
            return redirect('admin_panel')
    else:
        product_form = ProductForm()



    context = {'profile' : products,
               'product_form' : product_form
               }
    
    return render(request, 'admin_panel.html',context)

def index(request):
    products = Product.objects.all()
    context = {'product_list' : products}   
    return render(request, 'index.html',context)

def shop(request): 
    
    products = Product.objects.all()
    context = {'product_list' : products}   
    return render(request, 'shop.html',context)


def services(request): 
    
    products = Product.objects.all()
    context = {'product_list' : products}   
    return render(request, 'services.html',context)

def thankyou(request): 
    
    products = Product.objects.all()
    context = {'thankyou' : products}   
    return render(request, 'thankyou.html',context)


def contact(request): 
    
    products = Product.objects.all()
    context = {'contact' : products}   
    return render(request, 'contact.html',context)


def checkout(request): 
    
    reservations = Reservation.objects.filter(user= request.user , )
    print(reservations)
    context = {'reservations' : reservations}
    return render(request, 'checkout.html',context)


def about(request): 
    
    products = Product.objects.all()
    context = {'about' : products}   
    return render(request, 'about.html',context)


def blog(request):    
    return render(request, 'blog.html',)

def cart(request):
    reservations = Reservation.objects.filter(user= request.user , )
    print(reservations)
    context = {'reservations' : reservations}
    return render(request, 'cart.html',context)


@login_required
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)


@login_required
def reserve_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        form.fields["product_id"] = forms.IntegerField(widget=forms.HiddenInput(), initial=product_id)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            # Calculate total price based on the number of days
            total_price = (end_date - start_date).days * product.price_per_day

            # Create a reservation
            reservation = Reservation(
                user=request.user,
                product=product,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price
            )
            reservation.save()

            # Update availability
            availabilities = Availability.objects.filter(
                product=product,
                date__range=[start_date, end_date]
            )
            for availability in availabilities:
                availability.is_available = False
                availability.save()

            messages.success(request, 'Reservation successful!')
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid reservation input. Please check the selected dates.')

    # Render the reserve_product template with the product details and the reservation form
    context = {
        'product': product,
        'form': ReservationForm(),
    }
    return render(request, 'products/reserve_product.html', context)

def product_availability(request, product_id):
    product = Product.objects.get(id=product_id)
    availabilities = Availability.objects.filter(product=product)

    availability_data = {}
    for availability in availabilities:
        availability_data[str(availability.date)] = availability.is_available

    return JsonResponse(availability_data)


@login_required
def reservation_history(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    context = {
        'reservations': user_reservations,
    }
    return render(request, 'products/reservation_history.html', context)

ZARINPAL_API_ENDPOINT = "https://www.zarinpal.com/pg/rest/WebGate/"

@csrf_exempt
def initiate_payment(request, reservation_id):
    # Retrieve the reservation details from the database
    reservation = Reservation.objects.get(id=reservation_id)
    
    # Prepare the payment data
    data = {
        "MerchantID": "YOUR_MERCHANT_ID",
        "Amount": str(reservation.total_price),  # Total amount to be paid
        "Description": "Payment for rental reservation",
        "CallbackURL": "YOUR_CALLBACK_URL",
    }

    response = requests.post(ZARINPAL_API_ENDPOINT + "PaymentRequest.json", data=data)
    
    # Check the ZarinPal response
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("Status") == 100:
            # Payment request was successful, redirect the user to the ZarinPal payment page
            payment_url = "https://www.zarinpal.com/pg/StartPay/" + response_data.get("Authority")
            return JsonResponse({"payment_url": payment_url})
        else:
            messages.error(request, 'ZarinPal Payment Request Failed')
            return JsonResponse({"error": "ZarinPal Payment Request Failed"})
    else:
        return JsonResponse({"error": "Unable to connect to ZarinPal"})


@csrf_exempt
def verify_payment(request):

    if request.method == 'POST':
        # Retrieve the payment verification data from ZarinPal
        authority = request.POST.get('Authority')
        status = request.POST.get('Status')
        
        # Check if the payment was successful
        if status == 'OK':
            # Mark the reservation as paid and update its status
            reservation = Reservation.objects.get(id=request.POST.get('reservation_id'))
            reservation.is_paid = True
            reservation.save()
            return JsonResponse({"message": "Payment successful"})
        else:
            return JsonResponse({"error": "Payment failed"})
    else:
        return JsonResponse({"error": "Invalid request method"})
    



'''Ensure that you have properly configured email settings in your settings.py file,
 including your SMTP server details, email host, email credentials, etc.'''
def send_reservation_confirmation_email(user, reservation):
    subject = 'Reservation Confirmation'
    message = f'Hello {user.username}, your reservation for {reservation.product.name} is confirmed.'
    from_email = 'your_email@example.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)




def send_rental_reminder_email(user, reservation):
    subject = 'Upcoming Rental Reminder'
    message = f'Hello {user.username}, your rental for {reservation.product.name} starts on {reservation.start_date}.'
    from_email = 'your_email@example.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def send_reservation_change_notification(user, reservation):
    subject = 'Reservation Change Notification'
    message = f'Hello {user.username}, your reservation for {reservation.product.name} has been updated.'
    from_email = 'your_email@example.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

    
def serve_image(request,filename):
    image_path = os.path.join(settings.MEDIA_ROOT, 'product_images/'+filename)
    #print(image_path)
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), 'image/jpeg')
    

@login_required(login_url="/login/")
def serve_file(request,filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'files/'+filename)
    #print(image_path)
    with open(file_path, 'rb') as f:
        return HttpResponse(f.read(),content_type= 'pplication/octet-stream' )
