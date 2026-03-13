from rest_framework import serializers
from .models import Operator, Airport, FlightSource, Aircraft, Flight, EmptyLeg, Inquiry


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


class FlightSourceSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.name', read_only=True)

    class Meta:
        model = FlightSource
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    origin_display = serializers.SerializerMethodField()
    destination_display = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = '__all__'

    def get_origin_display(self, obj):
        if obj.origin:
            return f"{obj.origin.city} ({obj.origin.iata or obj.origin.icao})"
        return obj.origin_raw

    def get_destination_display(self, obj):
        if obj.destination:
            return f"{obj.destination.city} ({obj.destination.iata or obj.destination.icao})"
        return obj.destination_raw


class EmptyLegSerializer(serializers.ModelSerializer):
    origin_display = serializers.SerializerMethodField()
    destination_display = serializers.SerializerMethodField()
    aircraft_display = serializers.SerializerMethodField()
    operator_display = serializers.SerializerMethodField()
    source_name = serializers.CharField(source='source.name', read_only=True)
    inquiry_count = serializers.SerializerMethodField()

    class Meta:
        model = EmptyLeg
        fields = '__all__'

    def get_origin_display(self, obj):
        if obj.origin:
            return f"{obj.origin.city} ({obj.origin.iata or obj.origin.icao})"
        return obj.origin_raw

    def get_destination_display(self, obj):
        if obj.destination:
            return f"{obj.destination.city} ({obj.destination.iata or obj.destination.icao})"
        return obj.destination_raw

    def get_aircraft_display(self, obj):
        if obj.aircraft:
            return str(obj.aircraft)
        return obj.aircraft_raw

    def get_operator_display(self, obj):
        if obj.operator_company:
            return obj.operator_company.name
        return obj.operator

    def get_inquiry_count(self, obj):
        return obj.inquiries.count()


class EmptyLegPublicSerializer(serializers.ModelSerializer):
    """Serializer público: SIN precios"""
    origin_display = serializers.SerializerMethodField()
    destination_display = serializers.SerializerMethodField()
    aircraft_display = serializers.SerializerMethodField()
    has_discount = serializers.SerializerMethodField()

    class Meta:
        model = EmptyLeg
        fields = [
            'id', 'origin_display', 'destination_display',
            'departure_date', 'departure_time', 'flexible_dates',
            'aircraft_display', 'max_passengers',
            'has_discount', 'status', 'created_at',
        ]

    def get_origin_display(self, obj):
        if obj.origin:
            return f"{obj.origin.city} ({obj.origin.iata or obj.origin.icao})"
        return obj.origin_raw

    def get_destination_display(self, obj):
        if obj.destination:
            return f"{obj.destination.city} ({obj.destination.iata or obj.destination.icao})"
        return obj.destination_raw

    def get_aircraft_display(self, obj):
        if obj.aircraft:
            return str(obj.aircraft)
        return obj.aircraft_raw

    def get_has_discount(self, obj):
        return obj.discount_percent is not None and obj.discount_percent > 0


class InquirySerializer(serializers.ModelSerializer):
    empty_leg_display = serializers.SerializerMethodField()

    class Meta:
        model = Inquiry
        fields = '__all__'

    def get_empty_leg_display(self, obj):
        return str(obj.empty_leg)


class InquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['empty_leg', 'name', 'email', 'phone', 'message', 'passengers']
