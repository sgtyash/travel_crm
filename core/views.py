from datetime import timedelta

from django.contrib import messages
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML
from types import SimpleNamespace

from .forms import (
    CustomerForm,
    EnquiryForm,
    FerryLegForm,
    IslandStayForm,
    QuotationBuilderForm,
    DayPlanForm,
)
from .models import (
    ActivityRate,
    AgencySettings,
    Customer,
    DayPlan,
    Enquiry,
    Experience,
    FerryLeg,
    IslandStay,
    PhotoLibrary,
    Quotation,
)

IslandStayFormSet = inlineformset_factory(
    Quotation, IslandStay, form=IslandStayForm, extra=1, can_delete=True
)
FerryLegFormSet = inlineformset_factory(Quotation, FerryLeg, form=FerryLegForm, extra=1, can_delete=True)
DayPlanFormSet = inlineformset_factory(Quotation, DayPlan, form=DayPlanForm, extra=1, can_delete=True)


def home(request):
    return render(
        request,
        "core/home.html",
        {
            "customer_count": Customer.objects.count(),
            "quotation_count": Quotation.objects.count(),
        },
    )


def customer_list(request):
    return render(request, "core/customer_list.html", {"customers": Customer.objects.all()})


def customer_create(request):
    return customer_form(request)


def customer_edit(request, customer_id):
    return customer_form(request, get_object_or_404(Customer, pk=customer_id))


def customer_form(request, customer=None):
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == "POST" and form.is_valid():
        customer = form.save()
        messages.success(request, "Customer saved successfully.")
        return redirect("customer_edit", customer_id=customer.pk)

    return render(request, "core/customer_form.html", {"form": form, "customer": customer})


def enquiry_list(request):
    enquiries = Enquiry.objects.select_related("customer")
    search_term = request.GET.get("search", "").strip()
    customer_id = request.GET.get("customer", "")

    if search_term:
        enquiries = enquiries.filter(
            Q(destination__icontains=search_term) | Q(customer__name__icontains=search_term)
        )
    if customer_id:
        enquiries = enquiries.filter(customer_id=customer_id)

    return render(
        request,
        "core/enquiry_list.html",
        {
            "enquiries": enquiries,
            "customers": Customer.objects.all(),
            "selected_customer": customer_id,
            "search_term": search_term,
        },
    )


def enquiry_create(request):
    return enquiry_form(request)


def enquiry_edit(request, enquiry_id):
    return enquiry_form(request, get_object_or_404(Enquiry, pk=enquiry_id))


def enquiry_form(request, enquiry=None):
    form = EnquiryForm(request.POST or None, instance=enquiry)
    if request.method == "POST" and form.is_valid():
        enquiry = form.save()
        messages.success(request, "Enquiry saved successfully.")
        return redirect("enquiry_edit", enquiry_id=enquiry.pk)

    return render(request, "core/enquiry_form.html", {"form": form, "enquiry": enquiry})


def quotation_list(request):
    quotations = Quotation.objects.select_related("enquiry__customer")
    return render(request, "core/quotation_list.html", {"quotations": quotations})


def quotation_create(request):
    return redirect("quotation_new")


def quotation_detail(request, quotation_id):
    return redirect("quotation_edit", quotation_id=quotation_id)


def quotation_new(request):
    return quotation_builder(request)


def quotation_edit(request, quotation_id):
    quotation = get_object_or_404(Quotation, pk=quotation_id)
    return quotation_builder(request, quotation)


def quotation_enquiry_for(quotation, customer):
    if quotation.pk and quotation.enquiry_id and quotation.enquiry.customer_id == customer.pk:
        return quotation.enquiry

    destination = quotation.enquiry.destination if quotation.enquiry_id else "Travel package"
    start_date = quotation.arrival_date
    end_date = start_date + timedelta(days=max((quotation.nights or 1) - 1, 0))
    travel_type = "Premium Luxury" if quotation.package_tier == "Luxury+" else "Luxury"
    enquiry, _ = Enquiry.objects.get_or_create(
        customer=customer,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        adults=quotation.adults or 0,
        children=quotation.children or 0,
        travel_type=travel_type,
    )
    return enquiry


def quotation_builder(request, quotation=None):
    quotation_form = QuotationBuilderForm(request.POST or None, instance=quotation, prefix="quotation")
    island_formset = IslandStayFormSet(request.POST or None, instance=quotation, prefix="islands")
    ferry_formset = FerryLegFormSet(request.POST or None, instance=quotation, prefix="ferries")
    day_formset = DayPlanFormSet(request.POST or None, instance=quotation, prefix="days")
    formsets = [island_formset, ferry_formset, day_formset]

    form_is_valid = quotation_form.is_valid() if request.method == "POST" else False
    formsets_are_valid = all(formset.is_valid() for formset in formsets) if request.method == "POST" else False
    if request.method == "POST" and form_is_valid and formsets_are_valid:
        new_customer_name = quotation_form.cleaned_data["new_customer_name"].strip()
        customer = quotation_form.cleaned_data["customer"]
        if new_customer_name:
            customer = Customer.objects.filter(name__iexact=new_customer_name).first()
            if not customer:
                customer = Customer.objects.create(name=new_customer_name, phone="", email="")

        quotation = quotation_form.save(commit=False)
        if not customer:
            customer_name = quotation.guest_name.strip() or "Guest"
            customer = Customer.objects.filter(name__iexact=customer_name).first()
            if not customer:
                customer = Customer.objects.create(name=customer_name, phone="", email="")
        quotation.customer = customer
        quotation.children = quotation.children or 0
        quotation.enquiry = quotation_enquiry_for(quotation, customer)
        quotation.save()
        island_formset.instance = quotation
        ferry_formset.instance = quotation
        day_formset.instance = quotation
        island_formset.save()
        ferry_formset.save()
        day_formset.save()
        for form in day_formset.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE") and form.instance.pk:
                form.instance.photos.set(form.cleaned_data["photos"])
        messages.success(request, "Quotation saved successfully.")
        return redirect("quotation_edit", quotation_id=quotation.pk)

    photos = PhotoLibrary.objects.all()
    for form in day_formset.forms:
        selected_ids = {str(photo_id) for photo_id in form["photos"].value() or []}
        form.photo_options = [
            {"photo": photo, "selected": str(photo.pk) in selected_ids} for photo in photos
        ]
    empty_day_photo_options = [{"photo": photo, "selected": False} for photo in photos]

    return render(
        request,
        "core/quotation_builder.html",
        {
            "quotation": quotation,
            "quotation_form": quotation_form,
            "island_formset": island_formset,
            "ferry_formset": ferry_formset,
            "day_formset": day_formset,
            "empty_day_photo_options": empty_day_photo_options,
        },
    )


def quotation_pdf(request, quotation_id):
    quotation = get_object_or_404(
        Quotation.objects.select_related("enquiry__customer", "cover_photo", "break_photo"), pk=quotation_id
    )
    day_plans = DayPlan.objects.filter(quotation=quotation).prefetch_related("photos").order_by("day_number")
    island_stays = IslandStay.objects.filter(quotation=quotation).order_by("stay_order")
    ferry_legs = FerryLeg.objects.filter(quotation=quotation)
    agency_settings = AgencySettings.objects.select_related("closing_photo").first() or SimpleNamespace(
        agency_name="",
        logo=None,
        tagline="",
        welcome_message="",
        closing_message="",
        important_info="",
        inclusions="",
        exclusions="",
        payment_terms="",
        special_inclusions="",
        founder_signature="",
        contact_phone="",
        contact_email="",
        whatsapp_number="",
        closing_photo=None,
    )

    def lines_as_list(text):
        return [line.strip() for line in text.splitlines() if line.strip()] if text else []

    def information_boxes(text):
        labels = [
            "Flight",
            "Emergency",
            "Ferry",
            "Tourist Information",
            "Super Markets",
            "STD Code/GST Rates",
        ]
        content = {label: [] for label in labels}
        current_label = labels[0]
        for line in lines_as_list(text):
            heading, separator, detail = line.partition(":")
            matched_label = next(
                (label for label in labels if heading.strip().casefold() == label.casefold()),
                None,
            )
            if matched_label and separator:
                current_label = matched_label
                if detail.strip():
                    content[current_label].append(detail.strip())
            else:
                content[current_label].append(line)
        return [
            {"title": label, "content": "\n".join(content[label])}
            for label in labels
            if content[label]
        ] or [{"title": "Important Information", "content": text or "—"}]

    activity_rates = list(ActivityRate.objects.all())
    context = {
        "quotation": quotation,
        "agency_settings": agency_settings,
        "day_plans": day_plans,
        "island_stays": island_stays,
        "ferry_legs": ferry_legs,
        "activity_rate_pairs": [
            {"left": activity_rates[index], "right": activity_rates[index + 1] if index + 1 < len(activity_rates) else None}
            for index in range(0, len(activity_rates), 2)
        ],
        "experiences": Experience.objects.all(),
        "important_info_boxes": information_boxes(
            agency_settings.important_info
        ),
        "inclusions": lines_as_list(agency_settings.inclusions),
        "exclusions": lines_as_list(agency_settings.exclusions),
        "payment_terms": lines_as_list(agency_settings.payment_terms),
        "special_inclusions": lines_as_list(agency_settings.special_inclusions),
        "package_cost": f"{quotation.final_price:,.2f}" if quotation.final_price is not None else "—",
    }
    html = render_to_string("core/quotation_pdf.html", context)
    pdf = HTML(string=html, base_url=request.build_absolute_uri("/")).write_pdf()
    filename = slugify(quotation.enquiry.customer.name) or "customer"
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="quotation_{filename}.pdf"'
    return response
