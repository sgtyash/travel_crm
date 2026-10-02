from django.contrib import admin

from .models import (
    Activity,
    ActivityRate,
    AgencySettings,
    Customer,
    DayPlan,
    Enquiry,
    Experience,
    FerryLeg,
    Hotel,
    IslandStay,
    ItineraryDay,
    PhotoLibrary,
    Quotation,
    TransportItem,
)

admin.site.register(Customer)
admin.site.register(Enquiry)


class ItineraryDayInline(admin.TabularInline):
    model = ItineraryDay


class HotelInline(admin.TabularInline):
    model = Hotel


class TransportItemInline(admin.TabularInline):
    model = TransportItem


class ActivityInline(admin.TabularInline):
    model = Activity


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    inlines = [ItineraryDayInline, HotelInline, TransportItemInline, ActivityInline]


admin.site.register(ItineraryDay)
admin.site.register(Hotel)
admin.site.register(TransportItem)
admin.site.register(Activity)
admin.site.register(PhotoLibrary)
admin.site.register(IslandStay)
admin.site.register(FerryLeg)
admin.site.register(DayPlan)
admin.site.register(ActivityRate)
admin.site.register(Experience)


@admin.register(AgencySettings)
class AgencySettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AgencySettings.objects.exists()
