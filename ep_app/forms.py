from django import forms
from django.forms import fields
from ep_app import models

class DateInput(forms.DateInput):
    input_type = 'date'

class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    Confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = models.User
        fields = ( 'username','first_name', 'last_name', 'email', 'password',)

    def clean(self):
        cleaned_data = super(UserModelForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("Confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
    
class CitizenprofileModelForm(forms.ModelForm):
    class Meta():
        model = models.Citizenprofile
        fields = ('profile_pic','mobile_no','phone_no','dob','gender','address','City','state','pincode')
        widgets = {
            'dob': DateInput(),
            'address': forms.Textarea(attrs={'rows':3, 'cols':30})
        }
        

class Crime_CategoryModelForm(forms.ModelForm):
    class Meta():
        model = models.Crime_Category
        fields = '__all__'

class Crime_Sub_CategoryModelForm(forms.ModelForm):
    class Meta():
        model  = models.Crime_Sub_Category
        fields = '__all__'

class FirModelForm(forms.ModelForm):
    class Meta():
        model = models.Fir
        widgets = {
            'incident_place': forms.Textarea(attrs={'rows':3, 'cols':30}),
            'Crime_Description': forms.Textarea(attrs={'rows':4, 'cols':30}),
            'Fir_againts': forms.Textarea(attrs={'rows':4, 'cols':30}),
            'Date_and_Time': DateInput(),
        }
        fields = ('crime_category','crime_sub_category','incident_place','Date_and_Time','Crime_Description','Fir_againts','proof')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['crime_sub_category'].queryset = models.Crime_Sub_Category.objects.none()

        if 'crime_category' in self.data:
            try:
                crime_category_id = int(self.data.get('crime_category'))
                self.fields['crime_sub_category'].queryset = models.Crime_Sub_Category.objects.filter(crime_category_id=crime_category_id).order_by('crime_sub_category')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['crime_sub_category'].queryset = self.instance.Crime_Category.Crime_Sub_Category_set.order_by('crime_category')

class ComplainModelForm(forms.ModelForm):
    class Meta():
        model = models.Complain
        widgets = {
            'incident_place': forms.Textarea(attrs={'rows':3, 'cols':30}),
            'Crime_Description': forms.Textarea(attrs={'rows':4, 'cols':30}),
            'complain_againts': forms.Textarea(attrs={'rows':4, 'cols':30}),
            'Date_and_Time':DateInput(),
        }
        fields = ('incident_place','Date_and_Time','Crime_Description','complain_againts','proof')

class CityModelForm(forms.ModelForm):
    class Meta():
        model = models.City
        fields = '__all__'

class TalukaModelForm(forms.ModelForm):
    class Meta():
        model = models.Taluka
        fields = '__all__'

class VillageModelForm(forms.ModelForm):
    class Meta():
        model = models.Village
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['taluka'].queryset = models.Taluka.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['taluka'].queryset = models.Taluka.objects.filter(city_id=city_id).order_by('taluka')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['taluka'].queryset = self.instance.City.Taluka_set.order_by('city')

class Police_StationModelForm(forms.ModelForm):
    class Meta():
        model = models.Police_Station
        widgets = {
            'address': forms.Textarea(attrs={'rows':3, 'cols':30})
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['taluka'].queryset = models.Taluka.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['taluka'].queryset = models.Taluka.objects.filter(city_id=city_id).order_by('taluka')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['taluka'].queryset = self.instance.City.Taluka_set.order_by('city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['village'].queryset = models.Village.objects.none()

        if 'taluka' in self.data:
            try:
                taluka_id = int(self.data.get('taluka'))
                self.fields['village'].queryset = models.Village.objects.filter(taluka_id=taluka_id).order_by('village')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['village'].queryset = self.instance.Taluka.Village_set.order_by('taluka')

class Search_Police_StationModelForm(forms.ModelForm):
    class Meta():
        model = models.Police_Station
        fields = ('city','taluka','village')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['taluka'].queryset = models.Taluka.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['taluka'].queryset = models.Taluka.objects.filter(city_id=city_id).order_by('taluka')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['taluka'].queryset = self.instance.City.Taluka_set.order_by('city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['village'].queryset = models.Village.objects.none()

        if 'taluka' in self.data:
            try:
                taluka_id = int(self.data.get('taluka'))
                self.fields['village'].queryset = models.Village.objects.filter(taluka_id=taluka_id).order_by('village')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['village'].queryset = self.instance.Taluka.Village_set.order_by('taluka')
        
class FeedbackModelForm(forms.ModelForm):
    class Meta():
        model = models.Feedback
        widgets = {
            'Feedback': forms.Textarea(attrs={'rows':5, 'cols':35}),
        }
        fields = ('Feedback','Photo','Video')


#---------------------------------Inspector-Forms----------------------------------#

class Inspector_loginModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    Confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = models.Inspector_login
        fields = '__all__'

    def clean(self):
        cleaned_data = super(Inspector_loginModelForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("Confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class InspectorModelForm(forms.ModelForm):
    class Meta():
        model = models.Inspector
        fields = ('profile_pic','Age','date_of_birth','mobile_no','gender','address','city','state','pincode')
        widgets = {
            'date_of_birth': DateInput(),
        }


class Sub_InspectorModelForm(forms.ModelForm):
    class Meta():
        model = models.Sub_Inspector
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(),
        }

class ConstableModelForm(forms.ModelForm):
    class Meta():
        model = models.Constable
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(),
        }

class Service_OfficersModelForm(forms.ModelForm):
    class Meta():
        model = models.Service_Officers
        fields = '__all__'

#-------------------------------------INDEX_VIEW-------------------------------------------------#

class Missing_PersonsModelForm(forms.ModelForm):
    class Meta():
        model  = models.Missing_Persons
        widgets = {
            'Date_of_birth': DateInput(),
            'Missing_Date':DateInput(),
            'Address': forms.Textarea(attrs={'rows':3, 'cols':30})
        }
        fields = '__all__'

#-----------------------------------------------POLICE STATION---------------------------------------------------#

class Commissioner_loginModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    Confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = models.Commissioner_login
        fields = '__all__'

    def clean(self):
        cleaned_data = super(Commissioner_loginModelForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("Confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class CommissionerModelForm(forms.ModelForm):
    class Meta():
        model = models.Commissioner
        fields = ('profile_pic','Age','date_of_birth','mobile_no','gender','address','city','state','pincode')
        widgets = {
            'date_of_birth': DateInput(),
        }

class Emergency_InformationModelForm(forms.ModelForm):
    class Meta():
        model = models.Emergency_Information
        fields = '__all__'