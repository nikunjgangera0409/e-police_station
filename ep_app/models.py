from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class  Citizenprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic')
    GENDER_CHOICES = (('M', 'Male'),('F', 'Female'))
    mobile_no = models.IntegerField()
    phone_no = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    City = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()

    def __str__(self):
        return self.user.username

class City(models.Model):
    city = models.CharField(max_length=256)

    def __str__(self):
        return self.city
    
class Taluka(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    taluka = models.CharField(max_length=256)

    def __str__(self):
        return self.taluka

class Village(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE, null=True, blank=True)
    village = models.CharField(max_length=256)

    def __str__(self):
        return self.village

class Crime_Category(models.Model):
    crime_category = models.CharField(max_length=256)

    def __str__(self):
        return self.crime_category

class Crime_Sub_Category(models.Model):
    crime_category = models.ForeignKey(Crime_Category, on_delete=models.CASCADE)
    crime_sub_category = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.crime_sub_category

class Police_Station(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True)
    Police_station_name = models.CharField(max_length=200)
    address = models.TextField(max_length=200)
    phone_no = models.IntegerField(null=True, blank=True)
    mobile_no = models.IntegerField(null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.Police_station_name

    def get_absolute_url(self):
        return reverse('manage_police_station')

class Fir(models.Model):
    Satus_choices = (('Activate','Activate'),('Inprocess', 'Inprocess'),('Closed','Closed'))
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    police_station = models.ForeignKey(Police_Station, on_delete=models.CASCADE, null=True, blank=True)
    crime_category = models.ForeignKey(Crime_Category, on_delete=models.CASCADE, null=True , blank=True)
    crime_sub_category = models.ForeignKey(Crime_Sub_Category, on_delete=models.CASCADE, null=True , blank=True)
    incident_place = models.TextField()
    Date_and_Time = models.DateTimeField()
    Crime_Description = models.TextField()
    Fir_againts = models.TextField()
    proof = models.FileField(upload_to='proof', null=True , blank=True)
    status = models.CharField(max_length=20, choices=Satus_choices)
    Reason = models.CharField(max_length=256)
    FIR_Date_and_Time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username.username

    def get_absolute_url(self):
        return reverse('view_fir')

class Complain(models.Model):
    Satus_choices = (('Activate','Activate'),('Inprocess', 'Inprocess'),('Closed','Closed'))
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    police_station = models.ForeignKey(Police_Station, on_delete=models.CASCADE, null=True, blank=True)
    incident_place = models.TextField()
    Date_and_Time = models.DateTimeField( null=True,blank=True)
    Crime_Description = models.TextField()
    complain_againts = models.TextField()
    proof = models.FileField(upload_to='proof', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Satus_choices)
    Reason = models.CharField(max_length=256)
    complain_Date_and_Time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username.username

    def get_absolute_url(self):
        return reverse('view_complain')

class Feedback(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    Feedback = models.TextField()
    Photo = models.ImageField(upload_to = "photos_videos/", max_length=500 , null=True, blank=True)
    Video = models.FileField(upload_to="photos_videos/", max_length=500, null=True, blank=True)

    def __str__(self):
        return self.username.username


class Inspector_login(models.Model):
    username = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField()
    password = models.CharField(max_length = 20 , null=True,blank=True)

    def __str__(self):
        return self.username

class Inspector(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    user = models.OneToOneField(Inspector_login, on_delete=models.CASCADE)
    police_station = models.ForeignKey(Police_Station, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic')
    Age = models.IntegerField()
    date_of_birth = models.DateField()
    mobile_no = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()

    def __str__(self):
        return self.user.username

class Sub_Inspector(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='profile_pic')
    date_of_birth = models.DateField()
    mobile_no = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()

    def __str__(self):
        return self.username

class Constable(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='profile_pic')
    date_of_birth = models.DateField()
    mobile_no = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()

    def __str__(self):
        return self.username

class Service_Officers(models.Model):
    police_station = models.OneToOneField(Police_Station, on_delete=models.CASCADE)
    inspector = models.OneToOneField(Inspector_login, on_delete=models.CASCADE)
    sub_inspector = models.OneToOneField(Sub_Inspector, on_delete=models.CASCADE)
    constable = models.OneToOneField(Constable, on_delete=models.CASCADE)

    def __str__(self):
        return self.police_station.Police_station_name

class Missing_Persons(models.Model):
    Full_Name = models.CharField(max_length=256)
    Photo = models.ImageField(upload_to= 'missing_persons')
    Date_of_birth = models.DateField()
    Age = models.IntegerField()
    Nickname = models.CharField(max_length=256,blank=True,null=True)
    weight = models.IntegerField()
    height = models.CharField(max_length=10)
    Skin_color = models.CharField(max_length=256)
    Missing_Date = models.DateField()
    Address = models.TextField()
    Contact_no = models.BigIntegerField()

    def __str__(self):
        return self.Full_Name

class Rules_Regulations(models.Model):
    Title = models.CharField(max_length=256)
    Document = models.FileField(upload_to='rules_regulation')

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse('index')

class Commissioner_login(models.Model):
    username = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField()
    password = models.CharField(max_length = 20 , null=True,blank=True)

    def __str__(self):
        return self.username

class Commissioner(models.Model):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    user = models.OneToOneField(Commissioner_login, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic')
    Age = models.IntegerField()
    date_of_birth = models.DateField()
    mobile_no = models.IntegerField()
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()

    def __str__(self):
        return self.user.username

class Emergency_Information(models.Model):
    Name = models.CharField(max_length=200)
    Number = models.BigIntegerField()
