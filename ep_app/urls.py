from os import name
from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name='index'),
    path("add_missing_persons/",views.add_missing_persons,name = 'add_missing_persons'),
    path('Missing_PersonsListView/',views.Missing_PersonsListView.as_view(),name = 'Missing_PersonsListView'),
    path('Rules_RegulationsCreateView/',views.Rules_RegulationsCreateView.as_view(),name='Rules_RegulationsCreateView'),
    path('Rules_RegulationsListView/',views.Rules_RegulationsListView.as_view(),name = 'Rules_RegulationsListView'),
    path("Emergency_Information/",views.Emergency_Information,name="Emergency_Information"),
    path("Show_emergency/",views.Show_emergencyListView.as_view(),name = 'Show_emergency'),
#-----------------------------------------------------------------------------------------------------------#
    
    path('registration/', views.registration,name='registration'),
    path('otp_verify/',views.otp_verify, name = 'otp_verify'),
    path('citizen_login/',views.citizen_login,name='citizen_login'),
    path('citizen_logout/',views.citizen_logout,name='citizen_logout'),
    path('citizen_profile/',views.citizen_profile, name='citizen_profile'),
    path('view_citizen/',views.view_citizen,name='view_citizen'),
    path("update_citizen/<int:pk>",views.CitizenprofileUpdateView.as_view(),name="update_citizen"),
    path("citizen_password/",views.citizen_password,name = "citizen_password"),

    path("forgot_password/",views.forgot_password,name="forgot_password"),
    path("otp_password/",views.otp_password,name = "otp_password"),
    path("citinew_password/",views.citinew_password,name = "citinew_password"),
    
    path('file_fir/',views.file_fir,name='file_fir'),
    path('file_complain/',views.file_complain,name='file_complain'),
    path("fir_details/",views.fir_details,name = 'fir_details'),
    path("complain_details/",views.complain_details, name = "complain_details"),
    path('police_station/',views.police_station,name='police_station'),
    path('search_police_station/',views.search_police_station, name = 'search_police_station'),
    path('feedback/',views.feedback,name = 'feedback'),

#-------------------------------------------------------------------------------------------------------#

    path("login_details/",views.login_details,name ="login_details"),
    path("inspector_login/",views.inspector_login,name="inspector_login"),
    path("inspector_otp/",views.inspector_otp,name = "inspector_otp"),
    path("inspector_index/",views.inspector_index,name = "inspector_index"),
    path("inspector_logout/",views.inspector_logout,name = "inspector_logout"),
    path("inspector/",views.inspector,name = "inspector"),
    path("view_inspector/",views.view_inspector,name = 'view_inspector'),

    path("inspector_password/",views.inspector_password,name = "inspector_password"),
    path("update_inspector/<int:pk>",views.InspectorUpdateView.as_view(),name='update_inspector'),

    path("inspector_forgot/",views.inspector_forgot,name = 'inspector_forgot'),
    path("forgot_otp/",views.forgot_otp,name = "forgot_otp"),
    path("inspecnew_password/",views.inspecnew_password,name="inspecnew_password"),

#------------------------------------------------------------------------------------------------------#
    path("police_index/",views.police_index,name="police_index"),
    path("commissioner_login_details/",views.commissioner_login_details,name = "commissioner_login_details"),
    path("commissioner_login/",views.commissioner_login,name="commissioner_login"),
    path("commissioner_otp/",views.commissioner_otp,name="commissioner_otp"),
    path("commissioner_logout/",views.commissioner_logout,name="commissioner_logout"),
    path("commissioner/",views.commissioner,name='commissioner'),
    path("commissioner_view/",views.commissioner_view,name="commissioner_view"),
    path("commissioner_password/",views.commissioner_password,name='commissioner_password'),
    path("commissioner_update/<int:pk>/",views.commissioner_UpdateView.as_view(),name='commissioner_update'),

    path("commissioner_forgot/",views.commissioner_forgot,name="commissioner_forgot"),
    path("commissioner_forgot_otp/",views.commissioner_forgot_otp,name = "commissioner_forgot_otp"),
    path("commissionernew_password/",views.commissionernew_password,name="commissionernew_password"),

    path("manage_police_station/",views.manage_police_station,name="manage_police_station"),
    path("update_police_station/<int:pk>/",views.police_stationUpdateView.as_view(),name="update_police_station"),
    path("delete_police_station/<int:pk>/",views.police_stationDeleteView.as_view(),name ="delete_police_station"),

    path("manage_inspector/",views.manage_inspector,name='manage_inspector'),
    path("update_login_inspector/<int:pk>/",views.Inspector_loginUpdateview.as_view(),name="update_login_inspector"),
    path("Delete_login_inspector/<int:pk>",views.Inspector_loginDeleteView.as_view(),name = "Delete_login_inspector"),
    path("Details_inspector/<int:id>/",views.Details_inspector,name="Details_inspector"),

    path("manage_constable/",views.manage_constable,name = 'manage_constable'),
    path("update_constable/<int:pk>",views.constable_UpdateView.as_view(),name="update_constable"),
    path("delete_constable/<int:pk>",views.constable_DeleteView.as_view(),name = "delete_constable"),

    path("fir_details_view/",views.fir_details_view,name="fir_details_view"),
    path("complain_details_view/",views.complain_details_view,name="complain_details_view"),


    path("sub_inspector/",views.sub_inspector,name = "sub_inspector"),
    path("constable/",views.constable,name="constable"),
    path("service_officers/",views.service_officers,name = "service_officers"),


    path("view_fir/",views.view_fir, name = "view_fir"),
    path("view_complain/",views.view_complain, name = "view_complain"),
    path("manage_fir/",views.manage_fir, name="manage_fir"),
    path("manage_complain/",views.manage_complain, name="manage_complain"),
    path("fir_status/<int:pk>",views.FirUpdateView.as_view(),name="fir_status"),
    path("complain_status/<int:pk>/",views.ComplainUpdateView.as_view(),name="complain_status"),
    path("user_details/",views.user_details,name="user_details"),
 

#-------------------------------------------------------------------------------------------------------#

    path("crime_category/",views.crime_category,name = "crime_category"),
    path("crime_sub_category/",views.crime_sub_category,name = "crime_sub_category"),
    path("load_crime_sub_category/", views.load_crime_sub_category, name='load_crime_sub_category'), # AJAX

    path("city/",views.city, name= "city"),
    path("taluka/",views.taluka, name ="taluka"),
    path("village/",views.village, name = "village"),
    path("load_taluka/", views.load_taluka, name='load_taluka'), # AJAX
    path("load_village/",views.load_village,name = "load_village"), #AJAX

]