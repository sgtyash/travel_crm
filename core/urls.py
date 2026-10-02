from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/add/", views.customer_create, name="customer_create"),
    path("customers/<int:customer_id>/", views.customer_edit, name="customer_edit"),
    path("enquiries/", views.enquiry_list, name="enquiry_list"),
    path("enquiries/add/", views.enquiry_create, name="enquiry_create"),
    path("enquiries/<int:enquiry_id>/", views.enquiry_edit, name="enquiry_edit"),
    path("quotations/", views.quotation_list, name="quotation_list"),
    path("quotations/add/", views.quotation_create, name="quotation_create"),
    path("quotations/new/", views.quotation_new, name="quotation_new"),
    path("quotations/<int:quotation_id>/", views.quotation_detail, name="quotation_detail"),
    path("quotations/<int:quotation_id>/edit/", views.quotation_edit, name="quotation_edit"),
    path("quotations/<int:quotation_id>/pdf/", views.quotation_pdf, name="quotation_pdf"),
]
