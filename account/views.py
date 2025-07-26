from django.shortcuts import render , redirect
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser

# Create your views here.

class RegisterVeiw(View):
    template_name = 'core/index.html'

    def post( self, request):
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not email or not phone or not password1 or not password2:
            return render(request , self.template_name, {'error' : "فیلد هارو کامل وارد کنید"})

        if CustomUser.objects.filter(email=email).exists() :
            return render(request , self.template_name, {'error' : "ایمیل شما تکراری است و وجود دارد"})
        if password1 != password2 :
            return render(request , self.template_name, {'error' : "رمز عبور با تکرار رمز عبور مغایرت ندارد"})

        # ولیدشن شماره تلفن  
        # هش کردن پسورد
        user = CustomUser.objects.create(
                username = email,
                email = email,
                phone_number = phone,
                password = password1,
        )

        login(request , user)

        return redirect("core:home")
        

class LoginView(View):
    template_name = 'core/index.html'
    def post(self , request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request ,email=email , password=password)
        if user is not None:
            login(request, user)
            return redirect("core:home")
        else:
            
            return render(request, self.template_name, {"error": "ایمیل یا رمز عبور اشتباه است."})


class Logout(View):
    def get(self , request):
        logout(request)
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