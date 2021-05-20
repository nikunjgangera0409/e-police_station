from django import http
from django.core.checks import messages
from django.db.models import fields
from django.shortcuts import redirect, render
from django.http import HttpResponse , HttpResponseRedirect, request
from django.urls.base import reverse_lazy
from ep_app import forms, models
from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import UpdateView, ListView, CreateView, DeleteView, DetailView


def index(request):
    return render(request, 'index.html')

user = 0

def otp_verify(request):
    otp = request.POST.get('otp')
    uotp = request.POST.get('eotp')

    if otp == uotp:
        user.save()
        return HttpResponseRedirect(reverse('citizen_login'))
    else:
        return HttpResponse("<h1>OTP Verification Failed </h1>")

def registration(request):
    if request.method == 'POST':
        global user
        user = forms.UserModelForm(request.POST)
        otp = random.randint(111111,999999)
        if user.is_valid():
            mail = request.POST.get('email')
            pwd = request.POST.get('password')
            user = user.save(commit=False)
            user.set_password(pwd)
            send_mail(
                'OTP',
                f'Here is the otp to complete the registration {otp}.',
                settings.EMAIL_HOST_USER,
                [mail],
                fail_silently=False, )

            return render(request, 'citizen/otp.html', {'otp': otp})
    else:
        form = forms.UserModelForm()
        return render(request, 'citizen/user_registration.html', {'form':form})
    

def citizen_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpwd')
        try:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session['username'] = username
                    request.session['usr_login'] = True

                    return HttpResponseRedirect(reverse('index'))
        except:
            return HttpResponse("<h1>Username or Password is not valid</h1>")
    else:
        return render(request, 'citizen/login.html')

def citizen_logout(request):
    del request.session['usr_login']
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def citizen_profile(request):
    try:
        if request.method == 'POST':
            form = forms.CitizenprofileModelForm(request.POST, request.FILES)
            if form.is_valid():
                form_obj = form.save(commit=False)
                usr = request.session['username']
                user = models.User.objects.get(username=usr)
                form_obj.user = user

                if 'profile_pic' in request.FILES:
                    form_obj.profile_pic = request.FILES['profile_pic']

                form_obj.save()

                return HttpResponseRedirect(reverse('view_citizen')) 
            else:
                print(form.errors)
                return HttpResponse("Invalid form")
    except:
        return HttpResponse(f"<h1>Profile already save kindly visite view profile to update you profile</h1>")
    else:
        form = forms.CitizenprofileModelForm()
        return render(request, 'citizen/citizen_profile.html', {'form': form})

def citizen_password(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['c_password']:
            usr = request.session['username']
            password = request.POST['password']
            try:
                user = models.User.objects.get(username = usr)
                if user:
                    if user.is_active:
                        user.set_password(password)
                        user.save()
                        send_mail(
                            'Password Change',
                            f'Your password changed successfully..',
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False, )

                        return HttpResponseRedirect(reverse('citizen_logout'))
            except:
                return HttpResponse("<h1>User Not Valid...</h1>")
        else:
            return HttpResponse("Password and Confirm Password does not match..")
    else:
        return render(request, 'citizen/citizen_password.html')

def forgot_password(request):
    if request.method == "POST":
        user = request.POST['user']
        email = request.POST['email']
        otp = random.randint(111111,999999)
        try:
            username = models.User.objects.get(username=user,email=email)
            send_mail(
                'OTP for New Password',
                f'Here is your otp for new password: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False, )
            return render(request,'citizen/otp_password.html',{'otp':otp,'user':username})
        except:
            return HttpResponse("User Not Valid")
    else:
        return render(request,'citizen/citizen_forgot.html')

def otp_password(request):
    otp = request.POST.get('otp')
    uotp = request.POST.get('eotp')
    print(otp, uotp)
    email = request.POST['email']
    user = request.POST['user']
    if otp == uotp:
        return render(request, 'citizen/citinew_password.html',{'user':user,'email':email})
    else:
        return HttpResponse("<h1>OTP Verification Failed </h1>")


def citinew_password(request):
    user = request.POST['user']
    email = request.POST['email']
    try:
        username = models.User.objects.get(username=user,email = email)
        if request.POST['password'] == request.POST['c_password']:
            if username:
                if username.is_active:
                    username.set_password(request.POST['password'])
                    username.save()
                    send_mail(
                        'Password Change',
                        f'Your password changed successfully..',
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False, )

                    return HttpResponseRedirect(reverse('citizen_login'))
        else:
            return HttpResponse("<h1>Password and Confirm Password Does not match...</h1>")
    except:
        return HttpResponse("User Not Valid")


def view_citizen(request):
    try:
        usr = request.session['username']
        user = models.User.objects.get(username = usr)
        user_details = models.Citizenprofile.objects.get(user = user)
        return render(request,'citizen/view_citizen.html',{"user_details":user_details})
    except:
        return HttpResponse("<h1>Kindly Update your profile....</h1>")

class DateInput(forms.DateInput):
    input_type = 'date'

class CitizenprofileUpdateView(UpdateView):
    model = models.Citizenprofile
    fields = '__all__'
    template_name = 'citizen/update_citizen.html'

    def form_valid(self, form):
        username = self.request.session['username']
        email = models.User.objects.get(username = username)


        send_mail(
            'Profile Updated',
            f'hello...! {username} Your profile has beed updated.',
            settings.EMAIL_HOST_USER,
            [email.email],
            fail_silently=False, )

        form.save()
        return HttpResponseRedirect(reverse('view_citizen'))


def crime_category(request):
    if request.method == 'POST':
        form = forms.Crime_CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Crime Category Added...")
        else:
            print(form.errors)
            return HttpResponse("Invalid Form")
    else:
        form = forms.Crime_CategoryModelForm()
        return render(request , "police/crime_category.html",{"form":form})

def crime_sub_category(request):
    if request.method == 'POST':
        form = forms.Crime_Sub_CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Crime Sub Category Added...")
        else:
            print(form.errors)
            return HttpResponse("Invalid Form")
    else:
        form = forms.Crime_Sub_CategoryModelForm()
        return render(request , "police/crime_sub_category.html",{"form":form})

# AJAX
def load_crime_sub_category(request):
    crime_category_id = request.GET.get('crime_category_id')
    crime_sub_categories = models.Crime_Sub_Category.objects.filter(crime_category_id=crime_category_id).all()
    return render(request, 'police/crime_sub_category_dropdown_list.html', {'crime_sub_categories': crime_sub_categories})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

def file_fir(request):
    if request.method == 'POST':
        form = forms.FirModelForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            usr = request.session['username']
            user = models.User.objects.get(username=usr)
            form_obj.username = user
            mail = user.email
            ps = request.POST.get("ps_name")
            police_station_name = models.Police_Station.objects.get(Police_station_name=ps)
            email = models.Inspector.objects.get(police_station=police_station_name)
            form_obj.police_station = police_station_name

            if 'proof' in request.FILES:
                form_obj.proof = request.FILES['proof']

            form_obj.save()

            send_mail(
                'FIR Registered',
                f'hello...! {user} Your FIR is register. You will get the update shortly.',
                settings.EMAIL_HOST_USER,
                [mail],
                fail_silently=False, )
            
            send_mail(
                f'FIR Registred',
                f'hello...! {email.user} fir registered in your police station.',
                settings.EMAIL_HOST_USER,
                [police_station_name.email_address,email.user.email],
                fail_silently=False, )

            return HttpResponse('FIR Filed...')  
        else:
            print(form.errors)
            return HttpResponse("Invalid form")
    else:
        ps = request.GET.get("ps_name")
        fir = forms.FirModelForm()
        return render(request, 'services/fir_form.html',{'fir':fir,'ps':ps})

def file_complain(request):
    if request.method == 'POST':
        form = forms.ComplainModelForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            usr = request.session['username']
            user = models.User.objects.get(username=usr)
            form_obj.username = user
            mail = user.email
            ps = request.POST.get("ps_name")
            police_station_name = models.Police_Station.objects.get(Police_station_name=ps)
            email = models.Inspector.objects.get(police_station=police_station_name)
            form_obj.police_station = police_station_name


            if 'proof' in request.FILES:
                form_obj.proof = request.FILES['proof']
            
            form_obj.save()

            send_mail(
                'Complaint Registered',
                f'hello...! {user} Your complain is register. You will get the update shortly.',
                settings.EMAIL_HOST_USER,
                [mail],
                fail_silently=False, )

            send_mail(
                f'FIR Registred',
                f'hello...! {email.user} fir registered in your police station.',
                settings.EMAIL_HOST_USER,
                [police_station_name.email_address,email.user.email],
                fail_silently=False, )
                
            return HttpResponse('Complain Added...') 
        else:
            print(form.errors)
            return HttpResponse("Invalid form")
    else:
        ps = request.GET.get("ps_name")
        form = forms.ComplainModelForm()
        return render(request, 'services/complain_form.html',{'form':form,'ps':ps})


def search_police_station(request):
    if request.method == "POST":
        village_id = request.POST.get("village")
        police_station = models.Police_Station.objects.filter(village_id=village_id)
        form = forms.Search_Police_StationModelForm(request.POST)
        return render(request, "police/search_police_station.html",{'form':form,'police_station':police_station})
    else: 
        form = forms.Search_Police_StationModelForm()
        return render(request, 'police/search_police_station.html',{"form":form})


def feedback(request):
    if request.method == "POST":
        form = forms.FeedbackModelForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            usr = request.session['username']
            user = models.User.objects.get(username=usr)
            form_obj.username = user

            if 'Photo'  in request.FILES:
                form_obj.Photo = request.FILES['Photo']
            
            if 'Video' in request.FILES:
                form_obj.Video = request.FILES['Video']

            form_obj.save()
            return HttpResponse("Feedback Submited...")
        else:
            print(form.errors)
            return HttpResponse("Invalid Form")
    else:
        form = forms.FeedbackModelForm()
        show = models.Feedback.objects.all()
        return render(request, 'citizen/feedback.html',{"form":form,'show':show})


def fir_details(request):
    fir_detail = models.Fir.objects.all()
    return render(request, 'services/fir_details.html',{"fir_detail":fir_detail})


def complain_details(request):
    complain_detail = models.Complain.objects.all()
    return render(request, 'services/complain_details.html', {"complain_detail":complain_detail})


def city(request):
    if request.method == "POST":
        form = forms.CityModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("City Addedd...")
        else:
            print(form.errors)
            return HttpResponse("Invalid form...")
    else:
        form = forms.CityModelForm()
        return render(request, "police/city.html",{"form":form})

def taluka(request):
    if request.method == "POST":
        form = forms.TalukaModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Taluka Added...")
        else:
            print(form.errors)
            return HttpResponse("Invalid form...")
    else:
        form = forms.TalukaModelForm()
        return render(request,"police/taluka.html",{"form":form})

def village(request):
    if request.method == "POST":
        form = forms.VillageModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Village Added...")
        else:
            print(form.errors)
            return HttpResponse("Invalid form...")
    else:
        form = forms.VillageModelForm()
        return render(request, "police/village.html", {"form":form})

# Ajax
def load_taluka(request):
    city_id = request.GET.get('city_id')
    taluka = models.Taluka.objects.filter(city_id=city_id).all()
    return render(request, 'police/taluka_dropdown_list.html', {'taluka': taluka})

# Ajax
def load_village(request):
    taluka_id = request.GET.get('taluka_id')
    village = models.Village.objects.filter(taluka_id=taluka_id).all()
    return render(request, "police/village_dropdown_list.html",{"village":village})

######################################--INSPECTOR VIEWS--########################################################

def login_details(request):
    if request.method == "POST":
        form = forms.Inspector_loginModelForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            mail = request.POST.get("email")
            send_mail(
                "Inspector Login Details",
                f'Your username : {username} and Password : {password} to login as inspector.',
                settings.EMAIL_HOST_USER,
                [mail],
                fail_silently=False, )
            form.save()
            return HttpResponseRedirect(reverse('manage_inspector'))
        else:
            print(form.errors)
            return HttpResponse("Invalid form")
    else:
        form =forms.Inspector_loginModelForm()
        return render(request, 'inspector/login_details.html',{'form':form})


def inspector_otp(request):
    otp = request.POST.get('otp')
    uotp = request.POST.get('eotp')

    if otp == uotp:
        return HttpResponseRedirect(reverse('inspector_index'))
    else:
        return HttpResponse("<h1>OTP Verification Failed </h1>")

def inspector_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpwd')
        otp = random.randint(111111,999999)
        try:
            user = models.Inspector_login.objects.get(username=username,password=password)
            if user:
                email = models.Inspector_login.objects.get(username=username)
                mail= email.email

                send_mail(
                    'OTP',
                    f'hello...! {username} your 6 digit otp is {otp} to complete login.',
                    settings.EMAIL_HOST_USER,
                    [mail],
                    fail_silently=False, )
                
                request.session['username'] = username
                request.session['inspector_login'] = True
                return render(request, 'inspector/otp.html', {'otp': otp})
        except:
            return HttpResponse("<h1>Username or Password is not valid</h1>")
    else:
        return render(request, 'inspector/Inspector_login.html')

def inspector_index(request):
    return render(request , "Inspector/inspector_index.html")

def inspector_logout(request):
    del request.session['inspector_login']
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def inspector(request):
    try:
        if request.method == 'POST':
            form = forms.InspectorModelForm(request.POST, request.FILES)
            if form.is_valid():
                form_obj = form.save(commit=False)
                usr = request.session['username']
                user = models.Inspector_login.objects.get(username=usr)
                form_obj.user = user

                ps_name = models.Service_Officers.objects.get(inspector = user)
                police_station = models.Police_Station.objects.get(Police_station_name=ps_name)
                form_obj.police_station = police_station

                if 'profile_pic' in request.FILES:
                    form_obj.profile_pic = request.FILES['profile_pic']

                form_obj.save()
                return HttpResponse('Profile saved') 
            else:
                print(form.errors)
                return HttpResponse("Invalid form")
    except:
        return HttpResponse(f"<h1>Profile already save kindly visite view profile to update your profile</h1>")
    else:
        form = forms.InspectorModelForm()
        return render(request, 'inspector/inspector.html', {'form': form})

def view_inspector(request):
    try:
        usr = request.session['username']
        user = models.Inspector_login.objects.get(username = usr)
        user_details = models.Inspector.objects.get(user = user)
        return render(request,'inspector/view_inspector.html',{"user_details":user_details})
    except:
        return HttpResponse("Invalid User...")


def inspector_password(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['c_password']:
            usr = request.session['username']
            password = request.POST['password']
            print(password)
            user = models.Inspector_login.objects.get(username = usr)
            print(user)
            try:
                if user:
                    user.password = password
                    user.save()
                    send_mail(
                        'Password Change',
                        f'Your password changed successfully..',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False, )

                    return HttpResponseRedirect(reverse('inspector_logout'))
            except:
                return HttpResponse("<h1>User Not Valid...</h1>")
        else:
            return HttpResponse("Password and Confirm Password does not match..")
    else:
        return render(request, 'inspector/inspector_password.html')

def inspector_forgot(request):
    if request.method == "POST":
        user = request.POST['user']
        email = request.POST['email']
        otp = random.randint(111111,999999)
        try:
            username = models.Inspector_login.objects.get(username=user,email=email)
            send_mail(
                'OTP for New Password',
                f'Here is your otp for new password: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False, )
            return render(request,'inspector/forgot_otp.html',{'otp':otp,'user':username})
        except:
            return HttpResponse("User Not Valid")
    else:
        return render(request,'inspector/inspector_forgot.html')

def forgot_otp(request):
    otp = request.POST.get('otp')
    uotp = request.POST.get('eotp')
    email = request.POST['email']
    user = request.POST['user']
    if otp == uotp:
        return render(request, 'inspector/inspecnew_password.html',{'user':user,'email':email})
    else:
        return HttpResponse("<h1>OTP Verification Failed </h1>")

def inspecnew_password(request):
    user = request.POST['user']
    email = request.POST['email']
    if request.POST['password'] == request.POST['c_password']:
        try:
            username = models.Inspector_login.objects.get(username=user,email = email)
            if username:
                    username.password = request.POST['password']
                    username.save()
                    send_mail(
                        'Password Change',
                        f'Your password changed successfully..',
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False, )

                    return HttpResponseRedirect(reverse('inspector_login'))
        except:
            return HttpResponse("Invalid user...")
    else:
        return HttpResponse("<h1>Password and Confirm Password Does not match...</h1>")




class InspectorUpdateView(UpdateView):
    model = models.Inspector
    fields = '__all__'
    template_name = 'inspector/update_inspector.html'

    def form_valid(self, form):
        username = self.request.session['username']
        email = models.Inspector_login.objects.get(username = username)


        send_mail(
            'Profile Updated',
            f'hello...! {username} Your profile has beed updated.',
            settings.EMAIL_HOST_USER,
            [email.email],
            fail_silently=False, )

        form.save()
        return HttpResponseRedirect(reverse('view_inspector'))


def sub_inspector(request):
    if request.method =="POST":
        form = forms.Sub_InspectorModelForm(request.POST, request.FILES)
        if form.is_valid():
            
            if 'profile_pic' in request.FILES:
                form.profile_pic = request.FILES['profile_pic']
            form.save()
            return HttpResponse("Sub Inspector Added...")
        else:
            print(form.errors)
            return HttpResponse("Invalid form")
    else:
        form = forms.Sub_InspectorModelForm()
        return render(request, 'inspector/sub_inspector.html', {'form':form})

def constable(request):
    if request.method == "POST":
        form = forms.ConstableModelForm(request.POST, request.FILES)
        if form.is_valid():

            if 'profile_pic' in request.FILES:
                form.profile_pic = request.FILES['profile_pic']
            form.save()
            return HttpResponseRedirect(reverse('manage_constable'))

        else:
            print(form.errors)
            return HttpResponse("Invalid Form")
    else:
        form = forms.ConstableModelForm()
        return render(request, 'inspector/constable.html',{'form':form})

def service_officers(request):
    if request.method == "POST":
        form = forms.Service_OfficersModelForm(request.POST)
        if form.is_valid():
            police_station = request.POST.get("police_station")
            inspector = request.POST.get("inspector")
            sub_inspector = request.POST.get("sub_inspector")
            constable = request.POST.get("constable")

            ps_name = models.Police_Station.objects.get(id = police_station)
            ins_name = models.Inspector_login.objects.get(id = inspector)
            sins_name = models.Sub_Inspector.objects.get(id = sub_inspector)
            cons_name = models.Constable.objects.get(id = constable)
        
            send_mail(
                f'Service Officers of {ps_name}',
                f'''Incharge of police station is {ins_name.first_name} {ins_name.last_name}, 
                Sub Inspector {sins_name.first_name} {sins_name.last_name} 
                and constable {cons_name.first_name} {cons_name.last_name}''', 
                settings.EMAIL_HOST_USER,
                [ps_name.email_address,ins_name.email,sins_name.email,cons_name.email], 
                fail_silently=False)

            form.save()
            return HttpResponse("addedd...")
        else:
            print(form.errors)
            return HttpResponse("<h1>Service officers are already provided police station</h1>")
    else:
        form = forms.Service_OfficersModelForm()
        return render(request, 'police/service_officers.html',{'form':form})

def view_fir(request):
    usr = request.session["username"]
    user = models.Inspector_login.objects.get(username=usr)
    try:
        username = models.Inspector.objects.get(user = user)
        view_fir = models.Fir.objects.filter(police_station=username.police_station).all()
        return render(request, 'inspector/view_fir.html',{"view_fir":view_fir})
    except:
        return HttpResponse("<h1>Go to add profile and update your profile.</h1>")

def view_complain(request):
    usr = request.session["username"]
    user = models.Inspector_login.objects.get(username=usr)
    try:
        username = models.Inspector.objects.get(user = user)
        view_complain = models.Complain.objects.filter(police_station=username.police_station).all()
        return render(request, 'inspector/view_complain.html',{"view_complain":view_complain})
    except:
        return HttpResponse("<h1>Go to add profile and update your profile.</h1>")

def manage_fir(request):
    usr = request.session["username"]
    user = models.Inspector_login.objects.get(username=usr)
    try:
        username = models.Inspector.objects.get(user = user)
        manage_fir = models.Fir.objects.filter(police_station=username.police_station).all()
        return render(request, 'inspector/manage_fir.html',{"manage_fir":manage_fir})
    except:
        return HttpResponse("<h1>Go to add profile and update your profile.</h1>")


def manage_complain(request):
    usr = request.session["username"]
    user = models.Inspector_login.objects.get(username=usr)
    try:
        username = models.Inspector.objects.get(user = user)
        manage_complain = models.Complain.objects.filter(police_station=username.police_station).all()
        return render(request, 'inspector/manage_complain.html',{"manage_complain":manage_complain})
    except:
        return HttpResponse("<h1>Go to add profile and update your profile.</h1>")


class FirUpdateView(UpdateView):
    model = models.Fir
    fields = ('status', 'Reason')
    template_name = 'inspector/fir_status.html'

class ComplainUpdateView(UpdateView):
    model = models.Complain
    fields = ('status', 'Reason')
    template_name = 'inspector/complain_status.html'

def user_details(request):
    usr = request.session["username"]
    user = models.Inspector_login.objects.get(username=usr)
    try:
        username = models.Inspector.objects.get(user = user)
        complain_details = models.Complain.objects.filter(police_station=username.police_station).all()
        c_usr = models.Citizenprofile.objects.all()
        fir_details = models.Fir.objects.filter(police_station=username.police_station).all()
        return render(request , "inspector/user_details.html",{"complain_details":complain_details,"fir_details":fir_details,"c_usr":c_usr})
    except:
        return HttpResponse("<h1>Go to add profile and update your profile.</h1>")


#--------------------------------------------VISITOR_VIEW-----------------------------------------------------------#

def add_missing_persons(request):
    if request.method == 'POST':
        form = forms.Missing_PersonsModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Data Save...")
        else:
            print(form.errors)
            return HttpResponse("Form Invalid...")
    else:
        form = forms.Missing_PersonsModelForm()
        return render(request,'admin/add_missing_persons.html',{'form':form})

class Missing_PersonsListView(ListView):
    model = models.Missing_Persons
    template_name = 'visitor/missing_persons_list.html'

class Rules_RegulationsCreateView(CreateView):
    model = models.Rules_Regulations
    fields = '__all__'
    template_name = 'admin/rules_regulations.html'

class Rules_RegulationsListView(ListView):
    model = models.Rules_Regulations
    template_name = 'visitor/rules_regulations_list.html'

def Emergency_Information(request):
    if request.method == 'POST':
        form = forms.Emergency_InformationModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Data Save...")
        else:
            print(form.errors)
            return HttpResponse("Form Invalid...")
    else:
        form = forms.Emergency_InformationModelForm()
        return render(request,'admin/emergency_information.html',{'form':form})
    
class Show_emergencyListView(ListView):
    model = models.Emergency_Information
    template_name = 'visitor/Show_emergency.html'

#------------------------------------------POLICE_STATION---------------------------------------------------#


def police_index(request):
    return render(request,'police/police_station_index.html')


def commissioner_login_details(request):
    if request.method == "POST":
        form = forms.Commissioner_loginModelForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            mail = request.POST.get("email")
            send_mail(
                "Commissioner Login Details",
                f'Your username : {username} and Password : {password} to login in police station.',
                settings.EMAIL_HOST_USER,
                [mail],
                fail_silently=False, )
            form.save()
            return HttpResponse("Login Details Added..")
        else:
            print(form.errors)
            return HttpResponse("Invalid form")
    else:
        form =forms.Commissioner_loginModelForm()
        return render(request, 'police/commissioner_login_details.html',{'form':form})

def commissioner_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpwd')
        otp = random.randint(111111,999999)
        try:
            user = models.Commissioner_login.objects.get(username=username,password=password)
            if user:
                email = models.Commissioner_login.objects.get(username=username)
                mail= email.email

                send_mail(
                    'OTP',
                    f'hello...! {username} your 6 digit otp is {otp} to login in police station.',
                    settings.EMAIL_HOST_USER,
                    [mail],
                    fail_silently=False, )
                
                request.session['username'] = username
                request.session['commissioner_login'] = True
                return render(request, 'police/commissioner_otp.html', {'otp': otp})
        except:
            return HttpResponse("<h1>Username or Password is not valid</h1>")
    else:
        return render(request, 'police/commissioner_login.html')

def commissioner_otp(request):
    otp = request.POST.get('otp')
    uotp = request.POST.get('eotp')

    if otp == uotp:
        return HttpResponseRedirect(reverse('police_index'))
    else:
        return HttpResponse("<h1>OTP Verification Failed </h1>")

def commissioner(request):
    try:
        if request.method == 'POST':
            form = forms.CommissionerModelForm(request.POST, request.FILES)
            if form.is_valid():
                form_obj = form.save(commit=False)
                usr = request.session['username']
                user = models.Commissioner_login.objects.get(username=usr)
                form_obj.user = user

                if 'profile_pic' in request.FILES:
                    form_obj.profile_pic = request.FILES['profile_pic']

                form_obj.save()
                return HttpResponse('Profile saved') 
            else:
                print(form.errors)
                return HttpResponse("Invalid form")
    except:
        return HttpResponse(f"<h1>Profile already save kindly visite view profile to update you profile</h1>")
    else:
        form = forms.CommissionerModelForm()
        return render(request, 'police/commissioner.html', {'form': form})

def commissioner_view(request):
    usr = request.session['username']
    user = models.Commissioner_login.objects.get(username = usr)
    user_details = models.Commissioner.objects.get(user = user)
    return render(request,'police/view_commissioner.html',{"user_details":user_details})

def commissioner_password(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['c_password']:
            usr = request.session['username']
            password = request.POST['password']
            try:
                user = models.Commissioner_login.objects.get(username = usr)
                if user:
                    user.password = password
                    user.save()
                    send_mail(
                        'Password Change',
                        f'Your password changed successfully..',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False, )

                    return HttpResponseRedirect(reverse('commissioner_logout'))
            except:
                return HttpResponse("<h1>User Not Valid...</h1>")
        else:
            return HttpResponse("Password and Confirm Password does not match..")
    else:
        return render(request, 'police/commissioner_password.html')

class commissioner_UpdateView(UpdateView):
    model =models.Commissioner
    fields = '__all__'
    template_name = 'police/commissioner_update.html'
    success_url = reverse_lazy('commissioner_view')

def commissioner_forgot(request):
    if request.method == "POST":
        user = request.POST['user']
        email = request.POST['email']
        otp = random.randint(111111,999999)
        try:
            username = models.Commissioner_login.objects.get(username=user,email=email)
            send_mail(
                'OTP for New Password',
                f'Here is your otp for new password: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False, )
            return render(request,'police/commissioner_forgot_otp.html',{'otp':otp,'user':username})
        except:
            return HttpResponse("Invalid User")
    else:
        return render(request,'police/commissioner_forgot.html')

def commissioner_forgot_otp(request):
    otp = request.POST.get('otp')
    uotp = request.POST.get('eotp')
    email = request.POST['email']
    user = request.POST['user']
    if otp == uotp:
        return render(request, 'police/commissionernew_password.html',{'user':user,'email':email})
    else:
        return HttpResponse("<h1>OTP Verification Failed </h1>")

def commissionernew_password(request):
    user = request.POST['user']
    email = request.POST['email']
    if request.POST['password'] == request.POST['c_password']:
        try:
            username = models.Commissioner_login.objects.get(username=user,email = email)
            if username:
                    username.password = request.POST['password']
                    username.save()
                    send_mail(
                        'Password Change',
                        f'Your password changed successfully..',
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False, )

                    return HttpResponseRedirect(reverse('commissioner_login'))
        except:
            return HttpResponse("Invalid user...")
    else:
        return HttpResponse("<h1>Password and Confirm Password Does not match...</h1>")



def commissioner_logout(request):
    del request.session['commissioner_login']
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def police_station(request):
    if request.method == 'POST':
        form = forms.Police_StationModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manage_police_station'))
        else:
            print(form.errors)
            return HttpResponse("Invalid Form")
    else:
        form = forms.Police_StationModelForm()
        return render(request, 'police/police_station.html',{"form":form})


def manage_police_station(request):
    if request.method == "POST":
        village_id = request.POST.get("village")
        police_station = models.Police_Station.objects.filter(village_id=village_id)
        form = forms.Search_Police_StationModelForm(request.POST)
        return render(request, "police/manage_police_station.html",{'form':form,'police_station':police_station})
    else: 
        form = forms.Search_Police_StationModelForm()
        return render(request, 'police/manage_police_station.html',{"form":form})

class police_stationUpdateView(UpdateView):
    model = models.Police_Station
    fields = ('Police_station_name','address','phone_no','mobile_no','email_address')
    template_name = 'police/update_police_station.html'
    

class police_stationDeleteView(DeleteView):
    model = models.Police_Station
    template_name = 'police/delete_police_station.html'
    success_url = reverse_lazy('manage_police_station')

def manage_inspector(request):
    inspector = models.Inspector_login.objects.all()
    return render(request, 'police/manage_inspector.html',{'inspector':inspector})

class Inspector_loginUpdateview(UpdateView):
    model = models.Inspector_login
    fields = '__all__'
    template_name = 'police/update_login_inspector.html'
    success_url = reverse_lazy('manage_inspector')

class Inspector_loginDeleteView(DeleteView):
    model = models.Inspector_login
    template_name = 'police/delete_login_inspector.html'
    success_url = reverse_lazy('manage_inspector')

def Details_inspector(request,id):
    try:
        inspector = models.Inspector.objects.get(user = id)
        return render(request,'police/details_inspector.html',{'inspector':inspector})
    except:
        return HttpResponse("<h1>Profile not updated...</h1>")

def manage_constable(request):
    constable = models.Constable.objects.all()
    return render(request,'police/manage_constable.html',{'constable':constable})

class constable_UpdateView(UpdateView):
    model = models.Constable
    fields = '__all__'
    template_name = 'inspector/constable_update.html'
    success_url = reverse_lazy('manage_constable')

class constable_DeleteView(DeleteView):
    model = models.Constable
    template_name = 'inspector/constable_delete.html'
    success_url = reverse_lazy('manage_constable')

def fir_details_view(request):
    firs = models.Fir.objects.all()
    return render(request,'police/fir_details.html',{'firs':firs})

def complain_details_view(request):
    complains = models.Complain.objects.all()
    return render(request, 'police/complain_details.html',{'complains':complains})


