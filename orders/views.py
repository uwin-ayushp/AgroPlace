import urllib

import stripe
from django.shortcuts import render, redirect
from cart.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct
from app.models import Account
import datetime
import json
from django.http import JsonResponse, HttpResponseRedirect
from store.models import Product
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string
from django.views.generic import View
from django.urls import reverse
from django.conf import settings

def payments(request):
    body  = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderId'])
    payment =  Payment(
        user = request.user,
        payment_id = body['transId'],
        payment_method  = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    cart_items = CartItem.objects.filter(user=request.user)
    for item  in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id= order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save() 

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    CartItem.objects.filter(user=request.user).delete()

    # mail_subject = "Thank you for your order"
    # message = render_to_string('orders/ordered_recive_email.html',{'user': request.user,'order': order,})
    # to_email = request.user.email
    # send_email = EmailMessage(mail_subject,message,to=[to_email])
    # send_email.send()     

    data = {
        'order_number': order.order_number,
        'transId': payment.payment_id,
        
    }
    return render(request, 'orders/payments.html')







def place_order(request, total=0, quantity=0,):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
         return redirect('order_complete')
    for cart_item in cart_items:
        total += (cart_item.product.price *cart_item.quantity)
        quantity += cart_item.quantity
        product = Product.objects.get(id=cart_item.product.id)
        product.quantity -= cart_item.quantity
        product.save()

    if request.method == 'POST':
        
        data = Order()
        data.user = current_user
        data.first_name = request.POST.get("first_name","")
        data.last_name = request.POST.get("last_name","")
        data.phone_number = request.POST.get("phone_number","")
        data.email = request.POST.get("email","")
        data.address_line_1 = request.POST.get("address_line_1","")
        data.address_line_2 = request.POST.get("address_line_2","")
        data.country = request.POST.get("country","")
        data.state = request.POST.get("state","")
        data.city = request.POST.get("city","")
        data.order_note = request.POST.get("order_note","")
        data.ip = request.META.get("REMOTE_ADDR")
        data.farmer_id = product.farmerID
        data.save()
        data.order_total =total      
        data.save()
       
        """generating order number"""
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,  mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()
        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
        }
        return redirect(reverse("charge") + "?stripe_token=" + str(request.POST.get("stripe_token",""))+"&o_id="+str(order.id))
     
    else:
        form = OrderForm()
    return redirect('home')


class StripeAuthorizeView(View):

    def get(self, request):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        url = 'https://connect.stripe.com/oauth/authorize'
        params = {
            'response_type': 'code',
            'scope': 'read_write',
            'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
            'redirect_uri': f'http://localhost:8000/users/oauth/callback'
        }
        url = f'{url}?{urllib.parse.urlencode(params)}'
        return redirect(url)

def order_complete(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('created_at')
    context = {'orders':orders}
    print("test")
    return render(request, 'orders/payment_done.html', context)

class CourseChargeView(View):
    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the product using the 'stripe_token' parameter from the request
        # product = Product.objects.filter(id=request.GET.get('stripe_token')).first()
        # fee_percentage = 0.01 * int(product.price)
        # farmerId = product.farmerID
        # farmerEmail = Account.objects.filter(id=farmerId).first()
        o_id = request.GET.get('o_id')
        order = Order.objects.get(id=o_id)

        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            product = Product.objects.get(id=item.product_id)
            orderproduct.farmerID = product.farmerID
            orderproduct.save()
            # product = Product.objects.get(id=item.product_id)
            product.save()

        try:
            customer = get_or_create_customer(request.user.email, request.GET.get('stripe_token'))
            charge = stripe.Charge.create(
                amount=product.price * 100,  # Assuming price is in cents
                currency='cad',
                customer=customer.id,
                description=product.description,
                destination={
                    'amount': int(product.price),
                    'account': 'acct_1NuKJoEaf7EBKpF4'
                },
            )
            order_obj = Order.objects.get(id=o_id)

            if charge:
                order_obj.is_ordered = True
                order_obj.save()
                cart = CartItem.objects.filter(user=request.user)
                cart.delete()
                print("testing 1111")
                return JsonResponse({'status': 'success'}, status=202)
                # return redirect('order_complete')
            else:
                order_obj.delete()
                # Handle payment failure (e.g., show a message)
                return redirect('cart')
        except stripe.error.StripeError as e:
            # Handle Stripe error (e.g., show a message)
            return JsonResponse({'status': 'error'}, status=500)
# class CourseChargeView(View):
#
#     def get(self, request, *args, **kwargs):
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         # json_data = json.loads(request.body)
#         # product = Course.objects.filter(id=json_data['course_id']).first()
#         product = Product.objects.filter(id=request.GET.get('stripe_token'))
#         fee_percentage = .01 * int(product.price)
#         farmerId = product.farmerID
#         farmerEmail =  Account.objects.filter(id=farmerId)
#         o_id = request.GET.get('o_id')
#         order = Order.objects.get(id=o_id)
#
#         cart_items = CartItem.objects.filter(user=request.user)
#         for item in cart_items:
#             orderproduct = OrderProduct()
#             orderproduct.order_id = order.id
#             orderproduct.user_id = request.user.id
#             orderproduct.product_id = item.product_id
#             orderproduct.quantity = item.quantity
#             orderproduct.product_price = item.product.price
#             orderproduct.ordered = True
#             orderproduct.save()
#             product = Product.objects.get(id=item.product_id)
#             product.save()
#             try:
#                 customer = get_or_create_customer(
#                 self.request.user.email,
#                 request.GET.get('stripe_token'),
#                 )
#                 charge = stripe.Charge.create(
#                 amount=json_data['price'],
#                 currency='cad',
#                 customer=customer.id,
#                 description=json_data['description'],
#                 destination={
#                     'amount': int(json_data['price'] - (json_data['price'] * fee_percentage)),
#                     'account': 'acct_1NuKJoEaf7EBKpF4'
#                 },
#                 )
#                 order_obj = Order.objects.get(id=order_id)
#             if charge:
#                 order_obj.is_ordered = True
#                 order_obj.save()
#                 cart = CartItem.objects.filter(user=request.user)
#                 cart.delete()
#                 return redirect('order_complete')
#             else:
#                 order_obj.delete()
#                 # messages.warning(request, 'Payment failed. Please try again.')
#                 return redirect('cart')
#             # if charge:
#             #     return JsonResponse({'status': 'success'}, status=202)
#              except stripe.error.StripeError as e:
#              return JsonResponse({'status': 'error'}, status=500)

# helpers

def get_or_create_customer(email, token):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    connected_customers = stripe.Customer.list()
    for customer in connected_customers:
        if customer.email == email:
            print(f'{email} found')
            return customer
    print(f'{email} created')
    return stripe.Customer.create(
        email=email,
        source=token,
    )

class EsewaRequestView(View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get('o_id')
        order= Order.objects.get(id=o_id)

        cart_items = CartItem.objects.filter(user=request.user)
        for item  in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id= order.id
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save() 
            product = Product.objects.get(id=item.product_id)
            product.save() 

        context={"order":order}
        return render(request,'esewarequest.html',context)


class EsewaVerifyView(View):
    def get(self,request,*args,**kwargs):
        import xml.etree.ElementTree as ET
        oid=request.GET.get('oid')
        amt=request.GET.get('amt')
        refId=request.GET.get('refId')
        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid':refId ,
            'pid':oid,
        }
        resp = req.post(url, d)
        root = ET.fromstring(resp.content)
        status=root[0].text.strip()
        order_id=oid.split("_")[1]
        order_obj=Order.objects.get(id=order_id)
        if status == "Success":
            order_obj.is_ordered = True
            order_obj.save()
            cart = CartItem.objects.filter(user=request.user)
            cart.delete()
            return redirect('order_complete')
        else:
            order_obj.delete()
            messages.warning(request, 'Payment failed. Please try again.')
            return redirect('cart')