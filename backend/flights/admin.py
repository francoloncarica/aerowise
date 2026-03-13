from django.contrib import admin
from .models import Operator, Airport, FlightSource, Aircraft, Flight, EmptyLeg, Inquiry


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_type', 'country', 'city', 'is_active']
    list_filter = ['company_type', 'is_active', 'country']
    search_fields = ['name', 'city']


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['icao', 'iata', 'name', 'city', 'country']
    list_filter = ['country']
    search_fields = ['icao', 'iata', 'name', 'city']


@admin.register(FlightSource)
class FlightSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'operator', 'is_active', 'last_scraped', 'consecutive_errors']
    list_filter = ['source_type', 'is_active', 'requires_auth']
    search_fields = ['name']


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ['model', 'manufacturer', 'category', 'max_passengers']
    list_filter = ['category', 'manufacturer']
    search_fields = ['model', 'manufacturer']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['origin_raw', 'destination_raw', 'departure_time', 'status', 'source']
    list_filter = ['status', 'source']
    search_fields = ['origin_raw', 'destination_raw', 'flight_number']


@admin.register(EmptyLeg)
class EmptyLegAdmin(admin.ModelAdmin):
    list_display = [
        'origin_raw', 'destination_raw', 'departure_date',
        'price_usd', 'discount_percent', 'status', 'verified', 'published'
    ]
    list_filter = ['status', 'verified', 'published', 'source']
    search_fields = ['origin_raw', 'destination_raw', 'operator']
    list_editable = ['verified', 'published']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'empty_leg', 'status', 'passengers', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
