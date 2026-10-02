from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)  # Stores the customer's full name.
    phone = models.CharField(max_length=30)  # Stores a phone number for contact.
    email = models.EmailField()  # Stores a valid email address.
    notes = models.TextField(blank=True)  # Holds optional notes about the customer.
    created_at = models.DateTimeField(auto_now_add=True)  # Records when this customer was added.

    def __str__(self):
        return self.name


class Enquiry(models.Model):
    TRAVEL_TYPE_CHOICES = [
        ("Moderate", "Moderate"),
        ("Luxury", "Luxury"),
        ("Premium Luxury", "Premium Luxury"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Links this enquiry to a customer.
    destination = models.CharField(max_length=255)  # Stores the requested travel destination.
    start_date = models.DateField()  # Stores the planned departure date.
    end_date = models.DateField()  # Stores the planned return date.
    adults = models.IntegerField()  # Stores the number of adult travelers.
    children = models.IntegerField(default=0)  # Stores the number of child travelers.
    travel_type = models.CharField(max_length=20, choices=TRAVEL_TYPE_CHOICES)  # Stores the trip comfort level.
    created_at = models.DateTimeField(auto_now_add=True)  # Records when this enquiry was added.


class Quotation(models.Model):
    PACKAGE_TIER_CHOICES = [
        ("Luxury", "Luxury"),
        ("Luxury+", "Luxury+"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True
    )  # Stores the customer selected for this quotation.
    cover_photo = models.ForeignKey(
        "PhotoLibrary", on_delete=models.SET_NULL, null=True, blank=True
    )  # Stores the brochure cover image.
    break_photo = models.ForeignKey(
        "PhotoLibrary",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quotation_break_photos",
    )  # Stores the full-page scenic break image.
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE)  # Links this quotation to an enquiry.
    guest_name = models.CharField(max_length=255, blank=True)  # Stores the lead guest's name.
    adults = models.IntegerField(null=True, blank=True)  # Stores the number of adult guests.
    children = models.IntegerField(default=0)  # Stores the number of child guests.
    arrival_date = models.DateField(null=True, blank=True)  # Stores the date the guests arrive.
    nights = models.IntegerField(null=True, blank=True)  # Stores the package length in nights.
    days = models.IntegerField(null=True, blank=True)  # Stores the package length in days.
    flight_number = models.CharField(max_length=100, blank=True)  # Stores the arrival flight number.
    mattress_preference = models.CharField(max_length=100, blank=True)  # Stores the requested mattress style.
    persons_without_mattress = models.IntegerField(null=True, blank=True)  # Stores guests not needing a mattress.
    persons_with_mattress = models.IntegerField(null=True, blank=True)  # Stores guests needing a mattress.
    package_tier = models.CharField(
        max_length=20, choices=PACKAGE_TIER_CHOICES, blank=True
    )  # Stores the selected package tier.
    markup_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Stores a legacy markup amount.
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Stores the discount amount.
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Stores the package price entered by the agent.
    terms = models.TextField(blank=True)  # Holds optional quotation terms.
    created_at = models.DateTimeField(auto_now_add=True)  # Records when this quotation was added.

class ItineraryDay(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)  # Links this day to a quotation.
    day_number = models.IntegerField()  # Stores the day's number in the itinerary.
    title = models.CharField(max_length=255)  # Stores a short title for the day.
    description = models.TextField(blank=True)  # Holds optional details for the day.


class Hotel(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)  # Links this hotel to a quotation.
    hotel_name = models.CharField(max_length=255)  # Stores the hotel's name.
    city = models.CharField(max_length=255)  # Stores the hotel's city.
    room_type = models.CharField(max_length=100)  # Stores the selected room type.
    nights = models.IntegerField()  # Stores the number of hotel nights.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Stores the hotel price.


class TransportItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)  # Links this transport item to a quotation.
    transport_type = models.CharField(max_length=100)  # Stores the type of transport.
    route = models.CharField(max_length=255)  # Stores the travel route.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Stores the transport price.


class Activity(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)  # Links this activity to a quotation.
    activity_name = models.CharField(max_length=255)  # Stores the activity's name.
    description = models.TextField(blank=True)  # Holds optional activity details.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Stores the activity price.


class PhotoLibrary(models.Model):
    image = models.ImageField(upload_to="photo_library/")  # Stores an uploaded itinerary photo.


class AgencySettings(models.Model):
    agency_name = models.CharField(max_length=255, blank=True)  # Stores the agency display name.
    logo = models.ImageField(upload_to="agency/")  # Stores the agency logo.
    tagline = models.CharField(max_length=255)  # Stores the agency tagline.
    welcome_message = models.TextField(blank=True)  # Stores the brochure welcome letter.
    closing_message = models.TextField()  # Stores the brochure closing message.
    important_info = models.TextField()  # Stores important travel information.
    inclusions = models.TextField()  # Stores included package items.
    exclusions = models.TextField()  # Stores excluded package items.
    payment_terms = models.TextField()  # Stores payment and booking terms.
    special_inclusions = models.TextField(blank=True)  # Stores package special inclusions.
    founder_signature = models.CharField(max_length=255, blank=True)  # Stores the closing-page signature.
    contact_phone = models.CharField(max_length=100)  # Stores the agency phone number.
    contact_email = models.CharField(max_length=255)  # Stores the agency email address.
    whatsapp_number = models.CharField(max_length=100)  # Stores the agency WhatsApp number.
    closing_photo = models.ForeignKey(
        PhotoLibrary, on_delete=models.SET_NULL, null=True, blank=True
    )  # Stores the closing-page background image.

    def save(self, *args, **kwargs):
        if not self.pk and AgencySettings.objects.exists():
            raise ValueError("Only one AgencySettings record is allowed.")
        super().save(*args, **kwargs)


class ActivityRate(models.Model):
    name = models.CharField(max_length=255)  # Stores the activity rate name.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Stores the activity price.


class Experience(models.Model):
    name = models.CharField(max_length=255)  # Stores the experience name.
    price = models.CharField(max_length=255)  # Stores a single price or a price range.


class IslandStay(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)  # Links this stay to a quotation.
    island_name = models.CharField(max_length=255)  # Stores the island where guests stay.
    stay_order = models.IntegerField()  # Stores this stay's position in the trip.
    nights = models.IntegerField()  # Stores the number of nights on this island.
    hotel_name = models.CharField(max_length=255)  # Stores the booked hotel name.
    room_category = models.CharField(max_length=255)  # Stores the chosen room category.


class FerryLeg(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)  # Links this ferry ride to a quotation.
    from_island = models.CharField(max_length=255)  # Stores the departure island.
    to_island = models.CharField(max_length=255)  # Stores the arrival island.
    ferry_operator = models.CharField(max_length=255)  # Stores the ferry company.
    ferry_class = models.CharField(max_length=100)  # Stores the selected ferry class.


class DayPlan(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)  # Links this day plan to a quotation.
    day_number = models.IntegerField()  # Stores the day's number in the trip.
    day_title = models.CharField(max_length=255)  # Stores a short title for the day.
    morning_text = models.TextField(blank=True)  # Stores the morning plan.
    afternoon_text = models.TextField(blank=True)  # Stores the afternoon plan.
    evening_text = models.TextField(blank=True)  # Stores the evening plan.
    photos = models.ManyToManyField(PhotoLibrary, blank=True)  # Stores up to three selected day photos.
