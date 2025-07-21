from django.shortcuts import render , redirect
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from .models import *
# Create your views here.

class RegisterVeiw(View):
    

    def post( self, request):
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        print(email,phone,password1,password2)


        return redirect("core:home")
        


































# def 
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from .forms import CustomUserCreationForm
# from django.contrib import messages
# from django.contrib.auth import get_user_model

# User = get_user_model()  # استفاده از مدل CustomUser

# def register(request):
#     """ ثبت‌نام کاربر جدید با شماره تلفن، ایمیل و رمز عبور """
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # دریافت داده‌ها از فرم
#             email = form.cleaned_data['email']
#             phone = form.cleaned_data['phone']
#             password = form.cleaned_data['password1']

#             # چک کردن اینکه کاربر با این ایمیل قبلاً وجود دارد یا نه
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, "این ایمیل قبلاً ثبت شده است!")
#                 return render(request, 'accounts/register.html', {'form': form})

#             # ایجاد کاربر
#             user = form.save(commit=False)
#             user.set_password(password)
#             user.save()

#             # ورود خودکار
#             user = authenticate(username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('core:home')

#     else:
#         form = CustomUserCreationForm()

#     return render(request, 'accounts/register.html', {'form': form})