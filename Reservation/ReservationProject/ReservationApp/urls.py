from django.urls import path
from . import views

urlpatterns = [
    path('',views.Login,name='Login'),
    path("logout",views.Logout,name="Logout"),
    path('register',views.AccountRegistration.as_view(), name='register'),
    path("facility_select",views.facility_select,name="facility_select"),
    path("checklist/<str:facility_name>",views.checklist,name="checklist"),
    path("reservationlist",views.reservationlist,name="reservationlist"),
    path("detaillist/<int:reservation_id>",views.detaillist,name="detaillist"),
    path("delete/<str:reservation_id>",views.delete,name="delete"),
    path("update/<str:reservation_id>",views.update,name="update")
]
