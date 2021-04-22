import stripe 

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from .cart import Cart
from .forms import CheckoutForm

from apps.order.utilities import checkout, notify_customer, notify_vendor
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
def cart_detail(request):
    if request.user.customUser.role!='CUS' and request.user.customUser.role!='VEN':
        return render(request, 'core/accessdenied.html')

    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            try:
                # charge = stripe.Charge.create(
                #     amount=int(cart.get_total_cost() * 100),
                #     currency='USD',
                #     description='Charge from Interiorshop',
                #     source=stripe_token
                # )
                user = request.user
                first_name = user.first_name
                last_name = user.last_name
                email = user.email
                phone = user.customUser.contact
                address = user.customUser.address
                zipcode = user.customUser.zipcode

                print("user details")

                order = checkout(request, first_name, last_name, email, address, zipcode, "place", phone, cart.get_total_cost())

                print(order)
                cart.clear()

                notify_customer(order)
                notify_vendor(order)

                return redirect('success')
            except Exception as e:
                messages.error(request, 'There was something wrong with the payment')
                print("exception in payment", e)
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

def success(request):
    return render(request, 'cart/success.html')