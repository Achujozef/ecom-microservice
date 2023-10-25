import random
from django.shortcuts import render
import requests
from .models import * 
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views import View
from .forms import UserAddressForm

@never_cache
def user_login(request):
    if 'username' in request.session:
        return redirect('banner:base_file')
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = UserDetail.objects.get(uname=username)
        except UserDetail.DoesNotExist:
            messages.info(request, 'Invalid username or password')
            return redirect('user_login')
        
        if not user.uactive:
            messages.info(request, 'Your account has been blocked')
            return redirect('user_login')
        customer = UserDetail.objects.filter(uname=username).first()
        if not customer and password==customer.upassword:
            messages.info(request, 'Invalid username or passwordddddddddddd')
            return redirect('user_login')
        
        request.session['username'] = username
       
        # if 'guest_cart_id' in request.session:
        #     guest_cart_id = request.session['guest_cart_id']
        #     guest_user = UserDetail.objects.get(uname='guest')
        #     cart = NewCart.objects.get(cartid=guest_cart_id)

        #                     # Associate the cart items with the logged-in user
        #     cart.user = user
        #     cart.save()

        #                     # Clear the guest cart ID from the session
        #     del request.session['guest_cart_id']

        #     return redirect('checkout')
        
        return redirect('banner:base_file')

    return render(request, 'user_login.html')



@never_cache
def user_logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('otp_login')


def generate_otp():
    return str(random.randint(1000, 9999))


def send_otp(phone_num, otp):
    url = 'https://www.fast2sms.com/dev/bulkV2'
    payload = f'sender_id=TXTIND&message={otp}&route=v3&language=english&numbers={phone_num}'
    headers = {
        'authorization': "mEgP0Z5wnldKSerOu1GW8qUbVctH3jkYaM7QCI4Jzp69XNT2ALFmiofRb467D0rSOWVB3qp8J5HYeIvt",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def otp_login(request):
    
    if request.method == 'POST':
        phonenum = request.POST.get('phone')
        user_phonenum_list = UserDetail.objects.values_list('phone', flat=True)
        
        if phonenum not in user_phonenum_list:
            messages.error(request, 'Phone number not found. Please try again.')
            return render(request, 'mobile_otp.html')
        user = UserDetail.objects.get(phone=phonenum)
        if not user.uactive:
            messages.info(request, 'Your account has been blocked')
            return redirect('user_login')
        phonenum = request.POST.get('phone')
        otp = generate_otp()
        
        request.session['U_otp'] = otp
        request.session['U_phone'] = phonenum
        
        send_otp(phonenum, otp)
        
        return redirect('otp_verify')
    return render(request, 'mobile_otp.html')



def otp_verify(request):
    
    if 'U_otp' in request.session and 'U_phone' in request.session:
        exact_otp = request.session['U_otp']
        phonenum = request.session['U_phone']
        if request.method == 'POST':
           
            user_otp = request.POST.get('otp')
            if exact_otp == user_otp:
                try:
                    
                    user = UserDetail.objects.get(phone=phonenum)
                    
                    if user is not None:

                        request.session['username'] = user.uname 
                        request.session['phone'] = phonenum
                        messages.success(request, "Login completed successfully")
                        # if 'guest_cart_id' in request.session:
                        #     guest_cart_id = request.session['guest_cart_id']
                        #     guest_user = UserDetail.objects.get(uname='guest')
                        #     cart = NewCart.objects.get(cartid=guest_cart_id)

                        #     # Associate the cart items with the logged-in user
                        #     cart.user = user
                        #     cart.save()

                        #     # Clear the guest cart ID from the session
                        #     del request.session['guest_cart_id']

                        #     return redirect('checkout')
                        
                        return redirect('shop')
                except UserDetail.DoesNotExist:
                    messages.error(request, "This User doesn't Exist")
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        return render(request, 'user_otp.html', {'phonenum': phonenum})
    else:
        return redirect('otp_login')





@never_cache
def req_singup(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        uemail = request.POST.get('uemail')
        phone = request.POST.get('phone')
        upassword = request.POST.get('upassword')
        upassword2 = request.POST.get('upassword2')

        # Validation checks
        errors = {}

        if not uname.isalpha():
            errors['uname'] = 'Username should only contain alphabetic characters.'

        if uname.isspace() or len(uname) < 4:
            errors['uname'] = 'Username should be at least 4 characters long and should not contain only spaces.'

        if not phone.isdigit() or len(phone) != 10:
            errors['phone'] = 'Phone number should be a 10-digit number.'

        if len(upassword) < 8:
            errors['upassword'] = 'Password should be at least 8 characters long.'

        if upassword != upassword2:
            errors['upassword2'] = 'Passwords do not match.'

        # Check if username already exists
        try:
            existing_username = UserDetail.objects.get(uname=uname)
            errors['uname'] = 'Username already exists. Please choose another username.'
        except ObjectDoesNotExist:
            pass

        # Check if phone number already exists
        try:
            existing_phone = UserDetail.objects.get(phone=phone)
            errors['phone'] = 'Phone number already exists. Please choose another phone number.'
        except ObjectDoesNotExist:
            pass

        if errors:
            return render(request, 'singup.html', {'errors': errors})

        # Create a new UserDetail object
        user = UserDetail(uname=uname, uemail=uemail, phone=phone, upassword=upassword)
        user.save()

        # Create an empty Wallet for the user
        # wallet = Wallet(user=user, balance=Decimal('0.00'))
        # wallet.save()
        return redirect('user_login')

    return render(request, 'singup.html')

def admin_login(request):

    if 'adusername' in request.session:
        return redirect('admin_dash')
    if request.method =='POST':
        adusername=request.POST['adusername']
        adpassword=request.POST['adpassword']
        user = MyAdmin.objects.filter(username=adusername, password=adpassword).first()
        if user is not None:
            request.session['adusername']=adusername
            return redirect('admin_dash')
        else:
            messages.info(request,'Enter Valid User Name or Password')

    return render(request,'admin_login.html')

@never_cache
def admin_logout(request):
    if 'adusername' in request.session:
        del request.session['adusername']
    return redirect('admin_login')

def user_detail(request):

    users = UserDetail.objects.all()
    context = {'users': users}
    return render(request, 'admin_user.html', context)

def userblock(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        try:
            user = UserDetail.objects.get(id=uid)
        except UserDetail.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('user_detail')
        
        if user.uactive:
            user.uactive = False
            messages.warning(request, f'{user.uname} is blocked')
        else:
            user.uactive = True
            messages.success(request, f'{user.uname} is unblocked')
        user.save()
        # if request.session['user.username'] == user.uname:
        #     del request.session['user.username']
        return redirect('user_detail')
    else:
        return redirect('admin_login')

def userprofile(request):
    if 'username' in request.session:       
        user=request.session['username']
        profile=UserDetail.objects.get(uname=user)
        address=Address.objects.filter(user__uname=user).order_by('id')
        return render(request, 'userprofile.html',{'profile':profile,'address':address})
    else:
        return redirect('user_login')
    
class EditUserProfileView(View):
    def get(self, request):
        if 'username' in request.session:
            user = request.session['username']
            user = UserDetail.objects.get(uname=user)
            return render(request, 'edituserprofile.html', {'user': user})
        else:
            return redirect('user_login')

    def post(self, request):
        if 'username' in request.session:   
            user = request.session['username']
            user = UserDetail.objects.get(uname=user)
            uemail = request.POST.get('uemail')
            uphone = request.POST.get('uphone')
            UserDetail.objects.filter(uname=user.uname).update(uemail=uemail, phone=uphone)
            messages.success(request, 'User details updated successfully')
            return redirect('userprofile')
        else:
            return redirect('user_login')

class ChangePasswordView(View):
    def get(self, request):
        if 'username' in request.session:   
            return render(request,'changepassword.html')
        else:
            return redirect('user_login')   
    def post(self, request):
        if 'username' in request.session:
            user = request.session['username']
            user = UserDetail.objects.get(uname=user) 
            password = request.POST.get('upassword')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            if user.upassword == password:
                if pass1 == pass2:
                    if ' ' not in pass1:  # Check for spaces in the new password
                        user.upassword = pass1
                        user.save()
                        messages.success(request, "Passwords changed successfully")
                        return redirect('userprofile')
                    else:
                        messages.warning(request, "Passwords should not contain spaces")
                else:
                    messages.warning(request, "Passwords not matching")
            else:
                messages.warning(request, "Incorrect password")
            return redirect('changepassword')
        else:
            return redirect('user_login')

def updateprofileaddress(request,id):
    if 'username' in request.session:
        add = Address.objects.get(id=id)
        if request.method == 'POST':
            fm = UserAddressForm(request.POST, instance=add)
            if fm.is_valid():
                fm.save()
                messages.success(request,"Address updated successfully")
                return redirect('userprofile')
            else:
                return render(request, 'updateprofileaddress.html', {'fm': fm})
        else:
            fm = UserAddressForm(instance=add)
            return render(request, 'updateprofileaddress.html', {'fm': fm})
    else:
        return redirect('user_login')
    
def addprofileaddress(request):
    if 'username' in request.session:
        if request.method=='POST':
            fm = UserAddressForm(request.POST) 
            if fm.is_valid():
                use = request.session['username']
                user = UserDetail.objects.get(uname = use)
                reg = fm.save(commit=False)
                reg.user = user
                reg.save()
                messages.success(request, 'new address added successfully')
                return redirect('userprofile') 
            else:
                return render(request, 'addprofileaddress.html', {'fm': fm})
        else:
            fm = UserAddressForm()
            return render(request, 'addprofileaddress.html', {'fm': fm})
    else:
        return redirect('user_login')
    