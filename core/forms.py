from django import forms

from .models import (
    Activity,
    Customer,
    DayPlan,
    Enquiry,
    FerryLeg,
    Hotel,
    IslandStay,
    ItineraryDay,
    PhotoLibrary,
    Quotation,
    TransportItem,
)


class StyledModelForm(forms.ModelForm):
    """Adds Bootstrap classes to standard Django form controls."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                css_class = "form-select"
            else:
                css_class = "form-control"
            field.widget.attrs["class"] = css_class


class CustomerForm(StyledModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "email", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


class EnquiryForm(StyledModelForm):
    class Meta:
        model = Enquiry
        fields = ["customer", "destination", "start_date", "end_date", "adults", "children", "travel_type"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "adults": forms.NumberInput(attrs={"min": 1}),
            "children": forms.NumberInput(attrs={"min": 0}),
        }


class QuotationPricingForm(StyledModelForm):
    class Meta:
        model = Quotation
        fields = ["markup_amount", "discount_amount", "terms"]
        widgets = {
            "markup_amount": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
            "discount_amount": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
            "terms": forms.Textarea(attrs={"rows": 3}),
        }


class QuotationCreateForm(StyledModelForm):
    class Meta:
        model = Quotation
        fields = ["enquiry", "markup_amount", "discount_amount", "terms"]
        widgets = {
            "markup_amount": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
            "discount_amount": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
            "terms": forms.Textarea(attrs={"rows": 3}),
        }


class QuotationBuilderForm(StyledModelForm):
    new_customer_name = forms.CharField(required=False, label="New customer name")

    class Meta:
        model = Quotation
        fields = [
            "customer",
            "guest_name",
            "adults",
            "children",
            "arrival_date",
            "nights",
            "days",
            "flight_number",
            "mattress_preference",
            "persons_without_mattress",
            "persons_with_mattress",
            "package_tier",
            "final_price",
        ]
        widgets = {
            "adults": forms.NumberInput(attrs={"min": 1}),
            "children": forms.NumberInput(attrs={"min": 0}),
            "arrival_date": forms.DateInput(attrs={"type": "date"}),
            "nights": forms.NumberInput(
                attrs={"min": 0, "x-model.number": "nights", "@input": "syncDaysFromNights($event.target.value)"}
            ),
            "days": forms.NumberInput(
                attrs={"min": 1, "x-model.number": "days", "@input": "syncNightsFromDays($event.target.value)"}
            ),
            "persons_without_mattress": forms.NumberInput(attrs={"min": 0}),
            "persons_with_mattress": forms.NumberInput(attrs={"min": 0}),
            "final_price": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = field_name == "arrival_date"
        self.fields["customer"].empty_label = "Select customer"
        self.fields["package_tier"].choices = [
            ("", "Select tier"),
            *Quotation.PACKAGE_TIER_CHOICES,
        ]
        self.fields["customer"].widget.attrs.update(
            {
                "x-ref": "customerSelect",
                "@change": "$refs.guestName.value = $event.target.value ? $event.target.selectedOptions[0].text : ''",
            }
        )
        self.fields["guest_name"].widget.attrs["x-ref"] = "guestName"
        self.fields["new_customer_name"].widget.attrs.update(
            {
                "x-ref": "newCustomerName",
                "@input": "$refs.guestName.value = $event.target.value",
            }
        )



class ItineraryDayForm(StyledModelForm):
    class Meta:
        model = ItineraryDay
        fields = ["day_number", "title", "description"]
        widgets = {
            "day_number": forms.NumberInput(attrs={"min": 1}),
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class HotelForm(StyledModelForm):
    class Meta:
        model = Hotel
        fields = ["hotel_name", "city", "room_type", "nights", "price"]
        widgets = {
            "nights": forms.NumberInput(attrs={"min": 1}),
            "price": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
        }


class TransportItemForm(StyledModelForm):
    class Meta:
        model = TransportItem
        fields = ["transport_type", "route", "price"]
        widgets = {
            "price": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
        }


class ActivityForm(StyledModelForm):
    class Meta:
        model = Activity
        fields = ["activity_name", "description", "price"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "price": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
        }


class IslandStayForm(StyledModelForm):
    class Meta:
        model = IslandStay
        fields = ["island_name", "stay_order", "nights", "hotel_name", "room_category"]
        widgets = {
            "island_name": forms.TextInput(attrs={"list": "island-options"}),
            "stay_order": forms.NumberInput(attrs={"min": 1}),
            "nights": forms.NumberInput(attrs={"min": 1}),
        }


class FerryLegForm(StyledModelForm):
    class Meta:
        model = FerryLeg
        fields = ["from_island", "to_island", "ferry_operator", "ferry_class"]
        widgets = {
            "from_island": forms.TextInput(attrs={"list": "island-options"}),
            "to_island": forms.TextInput(attrs={"list": "island-options"}),
            "ferry_operator": forms.TextInput(attrs={"list": "ferry-operator-options"}),
            "ferry_class": forms.TextInput(attrs={"list": "ferry-class-options"}),
        }


class DayPlanForm(StyledModelForm):
    photos = forms.ModelMultipleChoiceField(queryset=PhotoLibrary.objects.none(), required=False)

    class Meta:
        model = DayPlan
        fields = ["day_number", "day_title", "morning_text", "afternoon_text", "evening_text"]
        widgets = {
            "day_number": forms.NumberInput(attrs={"min": 1}),
            "morning_text": forms.Textarea(attrs={"rows": 4}),
            "afternoon_text": forms.Textarea(attrs={"rows": 4}),
            "evening_text": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photos"].queryset = PhotoLibrary.objects.all()
        if self.instance.pk:
            self.initial["photos"] = self.instance.photos.all()

    def clean_photos(self):
        photos = self.cleaned_data["photos"]
        if photos.count() > 3:
            raise forms.ValidationError("Select no more than three photos for each day.")
        return photos
