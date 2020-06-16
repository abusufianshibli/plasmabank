from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import PlasmaDonor
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import login
from .tokens import account_activation_token
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView


# Create your views here.
def home (request):
    allDonor = PlasmaDonor.objects.all()
    context = {
        'allDonor': allDonor
    }
    return render(request, 'index.html', context)

def singin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        if username and password:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request,'you are login')
                return redirect('profile') 
            else:
                messages.error(request,' incorret Username Password!')
                return redirect('singin')   
        else:
            messages.error(request,'  Username & Password are invalid!')
            return redirect('singin')         
    return render(request,'singin.html')


def register (request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Taken')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists')
                return redirect('register')    
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    ) 
                user.is_active=False
            
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                })
                email_msg = EmailMessage(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                )
                email_msg.send()
                

            return redirect('singin')
        else:
            messages.error(request,' Password are not match!')
                    
    return render(request,'register.html')


@login_required()
def profile(request):
    if request.method == 'POST':
            name = request.POST.get('name')
            blood = request.POST.get('blood')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            status =request.POST.get('status')
            if PlasmaDonor.objects.filter(phone = phone).exists(): 
               messages.error(request,'You are already register!')
               return redirect('profile')
            else:
                plasmaDonor = PlasmaDonor(
                name = name,
                blood_group = blood,
                phone = phone,
                address = address,
                status = status,
                )
                plasmaDonor.save()
    return render(request,'profile.html')

def logout(request):
    auth.logout(request)
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('singin')
    else:
        return HttpResponse('Activation link is invalid!')

def delete_account(request,id):
    try:
        instance= PlasmaDonor.objects.get(id=id)
        instance.delete()
        print('donor deleted successfully!')
        return redirect('home')
    except:
        print('donor delete problem!')
        return redirect('profile')

class PasswordReset(PasswordResetView):
    template_name = 'password_reset.html'

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'