from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .forms import QuotationBuilderForm
from .models import (
    ActivityRate,
    AgencySettings,
    Customer,
    DayPlan,
    Enquiry,
    Experience,
    FerryLeg,
    IslandStay,
    Quotation,
)


class QuotationBuilderTests(TestCase):
    def setUp(self):
        customer = Customer.objects.create(
            name="Maya Patel",
            phone="555-0100",
            email="maya@example.com",
        )
        enquiry = Enquiry.objects.create(
            customer=customer,
            destination="Lisbon",
            start_date="2026-10-01",
            end_date="2026-10-07",
            adults=2,
            travel_type="Luxury",
        )
        self.quotation = Quotation.objects.create(
            customer=customer,
            enquiry=enquiry,
            guest_name="Maya Patel",
            adults=2,
            children=0,
            arrival_date="2026-10-01",
            nights=6,
            days=7,
            flight_number="TRV100",
            mattress_preference="Firm",
            package_tier="Luxury",
            final_price=Decimal("2500.00"),
        )

    def test_final_price_remains_the_manually_entered_package_price(self):
        self.quotation.save()

        self.assertEqual(self.quotation.final_price, Decimal("2500.00"))

    def test_quotation_edit_shows_the_guided_builder(self):
        response = self.client.get(reverse("quotation_edit", args=[self.quotation.pk]))

        self.assertContains(response, "Guest Details")
        self.assertContains(response, "Maya Patel")
        self.assertNotContains(response, 'name="quotation-enquiry"', html=False)
        self.assertContains(response, "Select customer")
        self.assertContains(response, "Select tier")
        self.assertNotContains(response, "- Select an option -")
        self.assertContains(response, "Island Stays")
        self.assertContains(response, "Ferry Legs")
        self.assertContains(response, "Day-by-Day Plan")
        self.assertContains(response, "Trip Duration")
        self.assertContains(response, "6N / 7D")

    def test_customer_string_representation_uses_the_customer_name(self):
        self.assertEqual(str(self.quotation.customer), "Maya Patel")

    def test_only_arrival_date_is_required_on_the_quotation_builder_form(self):
        form = QuotationBuilderForm()

        self.assertTrue(form.fields["arrival_date"].required)
        for field_name in [
            "nights",
            "days",
            "flight_number",
            "mattress_preference",
            "persons_without_mattress",
            "persons_with_mattress",
            "package_tier",
            "final_price",
            "children",
            "adults",
            "customer",
            "guest_name",
            "new_customer_name",
        ]:
            self.assertFalse(form.fields[field_name].required)

    def test_builder_saves_with_only_an_arrival_date(self):
        response = self.client.post(
            reverse("quotation_new"),
            {
                "quotation-arrival_date": "2026-10-01",
                "islands-TOTAL_FORMS": 0,
                "islands-INITIAL_FORMS": 0,
                "islands-MIN_NUM_FORMS": 0,
                "islands-MAX_NUM_FORMS": 1000,
                "ferries-TOTAL_FORMS": 0,
                "ferries-INITIAL_FORMS": 0,
                "ferries-MIN_NUM_FORMS": 0,
                "ferries-MAX_NUM_FORMS": 1000,
                "days-TOTAL_FORMS": 0,
                "days-INITIAL_FORMS": 0,
                "days-MIN_NUM_FORMS": 0,
                "days-MAX_NUM_FORMS": 1000,
            },
        )

        self.assertRedirects(response, reverse("quotation_edit", args=[2]))
        quotation = Quotation.objects.get(pk=2)
        self.assertEqual(quotation.arrival_date.isoformat(), "2026-10-01")
        self.assertEqual(quotation.customer.name, "Guest")
        self.assertIsNone(quotation.final_price)

    def test_ferry_operator_uses_the_requested_text_datalist(self):
        response = self.client.get(reverse("quotation_edit", args=[self.quotation.pk]))

        for option in ["Makruzz", "Nautika", "Green Ocean 1", "Green Ocean 2", "Govt Ferry"]:
            self.assertContains(response, f'<option value="{option}">', html=False)
        self.assertNotContains(response, "Government Ferry")
        self.assertNotContains(response, "ITT Majestic")
        self.assertContains(response, 'list="ferry-operator-options"', html=False)
        self.assertContains(response, 'list="ferry-class-options"', html=False)
        self.assertContains(response, '<option value="Premium">', html=False)
        self.assertContains(response, '<option value="Luxury">', html=False)

    def test_builder_saves_all_repeating_sections(self):
        response = self.client.post(
            reverse("quotation_new"),
            {
                "quotation-customer": "",
                "quotation-new_customer_name": "New Guest",
                "quotation-guest_name": "New Guest",
                "quotation-adults": 2,
                "quotation-children": 0,
                "quotation-arrival_date": "2026-10-01",
                "quotation-nights": 6,
                "quotation-days": 7,
                "quotation-flight_number": "TRV100",
                "quotation-mattress_preference": "Firm",
                "quotation-package_tier": "Luxury",
                "quotation-final_price": "2500.00",
                "islands-TOTAL_FORMS": 2,
                "islands-INITIAL_FORMS": 0,
                "islands-MIN_NUM_FORMS": 0,
                "islands-MAX_NUM_FORMS": 1000,
                "islands-0-island_name": "Port Blair",
                "islands-0-stay_order": 1,
                "islands-0-nights": 2,
                "islands-0-hotel_name": "Harbour Hotel",
                "islands-0-room_category": "Sea View",
                "islands-1-island_name": "Havelock Island",
                "islands-1-stay_order": 2,
                "islands-1-nights": 4,
                "islands-1-hotel_name": "Beach Resort",
                "islands-1-room_category": "Villa",
                "ferries-TOTAL_FORMS": 1,
                "ferries-INITIAL_FORMS": 0,
                "ferries-MIN_NUM_FORMS": 0,
                "ferries-MAX_NUM_FORMS": 1000,
                "ferries-0-from_island": "Port Blair",
                "ferries-0-to_island": "Havelock Island",
                "ferries-0-ferry_operator": "Makruzz",
                "ferries-0-ferry_class": "Premium",
                "days-TOTAL_FORMS": 2,
                "days-INITIAL_FORMS": 0,
                "days-MIN_NUM_FORMS": 0,
                "days-MAX_NUM_FORMS": 1000,
                "days-0-day_number": 1,
                "days-0-day_title": "Arrival",
                "days-0-morning_text": "Arrival",
                "days-0-afternoon_text": "Check in",
                "days-0-evening_text": "Dinner",
                "days-1-day_number": 2,
                "days-1-day_title": "Island day",
                "days-1-morning_text": "Breakfast",
                "days-1-afternoon_text": "Beach time",
                "days-1-evening_text": "Sunset",
            },
        )

        self.assertRedirects(response, reverse("quotation_edit", args=[2]))
        quotation = Quotation.objects.get(pk=2)
        self.assertEqual(quotation.customer.name, "New Guest")
        self.assertEqual(quotation.enquiry.customer, quotation.customer)
        self.assertEqual(quotation.nights, 6)
        self.assertEqual(quotation.days, 7)
        self.assertEqual(IslandStay.objects.filter(quotation=quotation).count(), 2)
        self.assertEqual(FerryLeg.objects.filter(quotation=quotation).count(), 1)
        self.assertEqual(DayPlan.objects.filter(quotation=quotation).count(), 2)

    def test_quotation_pdf_downloads_a_pdf(self):
        DayPlan.objects.create(
            quotation=self.quotation,
            day_number=1,
            day_title="Arrival in Port Blair",
            morning_text="Arrival",
            afternoon_text="Hotel check-in",
            evening_text="Welcome dinner",
        )
        IslandStay.objects.create(
            quotation=self.quotation,
            island_name="Port Blair",
            stay_order=1,
            nights=2,
            hotel_name="Harbour Hotel",
            room_category="Sea View",
        )
        FerryLeg.objects.create(
            quotation=self.quotation,
            from_island="Port Blair",
            to_island="Havelock Island",
            ferry_operator="Makruzz",
            ferry_class="Premium",
        )
        ActivityRate.objects.create(name="Glass-bottom boat", price=Decimal("1200.00"))
        Experience.objects.create(name="Scuba diving", price="2000/3000")

        response = self.client.get(reverse("quotation_pdf", args=[self.quotation.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("attachment; filename=", response["Content-Disposition"])
        self.assertTrue(response.content.startswith(b"%PDF"))

    def test_agency_settings_allows_only_one_record(self):
        AgencySettings.objects.create(
            logo="agency/logo.png",
            tagline="Island journeys",
            closing_message="We look forward to welcoming you.",
            important_info="Carry valid identification.",
            inclusions="Accommodation",
            exclusions="Flights",
            payment_terms="Balance due before travel.",
            contact_phone="+00 000 000 000",
            contact_email="travel@example.com",
            whatsapp_number="+00 000 000 000",
        )

        with self.assertRaises(ValueError):
            AgencySettings.objects.create(
                logo="agency/another-logo.png",
                tagline="Another agency",
                closing_message="Message",
                important_info="Info",
                inclusions="Inclusion",
                exclusions="Exclusion",
                payment_terms="Terms",
                contact_phone="Phone",
                contact_email="email@example.com",
                whatsapp_number="WhatsApp",
            )
