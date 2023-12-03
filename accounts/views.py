from django.shortcuts import render, redirect, get_object_or_404

import farmer.models
from orders.models import Order, OrderProduct
from .forms import RegistrationForm, UserForm, UserProfileForm
from app.models import Account, UserProfile
# from orders.models import Order, OrderProduct
# from cart.models import Cart, CartItem
# from cart.views import _cart_id
import requests
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
"""verification email"""
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from accounts.models import Chatbox
from django.utils import timezone

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            email = form.cleaned_data['email']
            username = email.split('@')[0]
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            userRole = request.POST.get('userType')
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                               email=email, password=password, user_role=userRole)
            user.phone_number = phone_number
            user.is_active = True
            user.save()

            # creating a user profile

            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_pic = 'default/default-user.png'
            profile.save()

            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now loged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)

            except:
                return redirect('dashbord')

        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url=login)
def logout(request):
    auth.logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'congratulations your account is actived')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashbord(request):
    user = Account.objects.get(email=request.user.email)
    orders_count = ''
    orders =''
    ulist = ''
    if user.user_role == 'farmer':
        orders = Order.objects.order_by('created_at').filter(farmer_id=request.user.id, is_ordered=True)
        ulist = Account.objects.filter(user_role='specialist')
        orders_count = orders.count()
    elif user.user_role == 'buyer':
        orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
        orders_count = orders.count()
    else:

        distinct_farmer_ids = Chatbox.objects.order_by('-created_date').filter(sp_id=user.id).values_list('farmer_id',
                                                                                        flat=True).distinct()

        # Filter Account objects based on the distinct farmer IDs
        ulist = Account.objects.filter(id__in=distinct_farmer_ids)
        orders_count = ulist.count()


    context = {
        'orders': orders,
        'orders_count': orders_count,
        'ulist': ulist
    }
    return render(request, 'accounts/dashbord.html', context)


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            """reset password"""
            current_site = get_current_site(request)
            mail_subject = "Please reset your password"
            message = render_to_string('accounts/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)

            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'password reset email has been sent')
            return redirect('login')

        else:
            messages.error(request, 'account dose not exists')
            return redirect('forgot-password')

    return render(request, 'accounts/forgotPassword.html')


def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):

        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'reset your password')
        return redirect('reset-password')
    else:
        messages.error(request, 'this link has expired')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password has been reset')
            return redirect('login')

        else:
            messages.error(request, 'password do not match')
            return redirect('reset-password')
    else:
        return render(request, 'accounts/resetPassword.html')


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-status','created_at')
    context = {
        'orders': orders
    }
    print(orders)
    return render(request, 'accounts/my_orders.html', context)


def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'your profile has been updated')
            return redirect('edit_profile')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }
    return render(request, 'accounts/edit_profile.html', context)

def chatbox(request,id):

    user = Account.objects.get(email=request.user.email)
    if user.user_role=='farmer':
        farmerid = user.id
        spId = id

    elif user.user_role=='specialist':
        spId= user.id
        farmerid = id

    chat_history = Chatbox.objects.filter(
        (Q(sp_id=spId, farmer_id=farmerid) | Q(sp_id=farmerid, farmer_id=spId))
    ).distinct().order_by('created_date')

    context = {
        'id': id,
        'uid':user.id,
        'chat_history': chat_history,
    }
    return render(request, 'accounts/chatbox.html',context)

# def sendMsg(request):
#     if request.method == 'POST':
#         Recieverid = request.POST.get('id')
#         print(Recieverid)
#
#         senderId = request.user.id
#         message_text = request.POST.get('msg')
#
#         # Save the message to the Chatbox model
#         cbox= Chatbox()
#
#         cbox.sp_id= Recieverid
#         cbox.farmer_id=senderId
#         cbox.text=message_text
#         cbox.senderid = senderId
#         cbox.recid = Recieverid
#         cbox.created_date=timezone.now()
#         cbox.save()
#         return redirect('chatbox', id=Recieverid)
#     else:
#         # Handle other cases if necessary
#         pass

def sendMsg(request):
    if request.method == 'POST':
        receiver_id = int(request.POST.get('id'))
        sender_id = request.user.id
        message_text = request.POST.get('msg')

        chatbox_instance = Chatbox(
                sp_id=receiver_id,
                farmer_id=sender_id,
                senderid=sender_id,
                recid=receiver_id,
                text=message_text,
                created_date=timezone.now()
        )
        chatbox_instance.save()

        return redirect('chatbox', id=receiver_id)
    else:
        # Handle other cases if necessary
        pass
@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)
