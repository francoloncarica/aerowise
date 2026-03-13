from django.db import models
from django.utils import timezone
from datetime import date


class Operator(models.Model):
    COMPANY_TYPE_CHOICES = [
        ('operator', 'Operador'),
        ('broker', 'Broker'),
    ]

    name = models.CharField(max_length=200, unique=True)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, default='operator')
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Operador'
        verbose_name_plural = 'Operadores'

    def __str__(self):
        return self.name


class Airport(models.Model):
    icao = models.CharField(max_length=4, unique=True, db_index=True)
    iata = models.CharField(max_length=3, db_index=True, blank=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['icao']
        verbose_name = 'Aeropuerto'
        verbose_name_plural = 'Aeropuertos'

    def __str__(self):
        iata_str = f" ({self.iata})" if self.iata else ""
        return f"{self.icao}{iata_str} — {self.city}, {self.country}"


class FlightSource(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('web_public', 'Web Pública'),
        ('web_private', 'Web Privada'),
        ('api', 'API'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('manual', 'Manual'),
    ]

    name = models.CharField(max_length=200, unique=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES, default='web_public')
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='sources')
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    scrape_interval_minutes = models.PositiveIntegerField(default=60)
    last_scraped = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    consecutive_errors = models.PositiveIntegerField(default=0)
    config = models.JSONField(default=dict, blank=True)
    requires_auth = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Fuente de Datos'
        verbose_name_plural = 'Fuentes de Datos'

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"

    def record_success(self):
        self.last_scraped = timezone.now()
        self.last_error = ''
        self.consecutive_errors = 0
        self.save(update_fields=['last_scraped', 'last_error', 'consecutive_errors'])

    def record_error(self, msg):
        self.last_error = str(msg)[:500]
        self.consecutive_errors += 1
        self.save(update_fields=['last_error', 'consecutive_errors'])

    def reset_errors(self):
        self.last_error = ''
        self.consecutive_errors = 0
        self.save(update_fields=['last_error', 'consecutive_errors'])


class Aircraft(models.Model):
    CATEGORY_CHOICES = [
        ('light', 'Light Jet'),
        ('midsize', 'Midsize Jet'),
        ('super_midsize', 'Super Midsize Jet'),
        ('heavy', 'Heavy Jet'),
        ('ultra_long', 'Ultra Long Range'),
        ('turboprop', 'Turboprop'),
        ('helicopter', 'Helicóptero'),
        ('other', 'Otro'),
    ]

    model = models.CharField(max_length=200, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    max_passengers = models.PositiveIntegerField(null=True, blank=True)
    range_km = models.PositiveIntegerField(null=True, blank=True)
    cruise_speed_kmh = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['model']
        verbose_name = 'Aeronave'
        verbose_name_plural = 'Aeronaves'

    def __str__(self):
        return f"{self.manufacturer} {self.model}" if self.manufacturer else self.model


class Flight(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Programado'),
        ('en_route', 'En Ruta'),
        ('landed', 'Aterrizado'),
        ('cancelled', 'Cancelado'),
        ('unknown', 'Desconocido'),
    ]

    flight_number = models.CharField(max_length=20, blank=True)
    callsign = models.CharField(max_length=20, blank=True)
    registration = models.CharField(max_length=20, blank=True)
    source = models.ForeignKey(FlightSource, on_delete=models.CASCADE, related_name='flights')
    external_id = models.CharField(max_length=200, blank=True, db_index=True)
    origin = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, blank=True, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, blank=True, related_name='arrivals')
    origin_raw = models.CharField(max_length=200, blank=True)
    destination_raw = models.CharField(max_length=200, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True)
    aircraft_raw = models.CharField(max_length=200, blank=True)
    operator = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unknown')
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-departure_time']
        verbose_name = 'Vuelo'
        verbose_name_plural = 'Vuelos'
        constraints = [
            models.UniqueConstraint(
                fields=['source', 'external_id'],
                condition=~models.Q(external_id=''),
                name='unique_flight_source_external_id'
            )
        ]

    def __str__(self):
        origin = self.origin_raw or str(self.origin) if self.origin else '?'
        dest = self.destination_raw or str(self.destination) if self.destination else '?'
        return f"{origin} → {dest} ({self.departure_time})"


class EmptyLeg(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('booked', 'Reservado'),
        ('expired', 'Expirado'),
        ('cancelled', 'Cancelado'),
    ]

    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True, related_name='empty_legs')
    source = models.ForeignKey(FlightSource, on_delete=models.CASCADE, related_name='empty_legs')
    external_id = models.CharField(max_length=200, blank=True, db_index=True)
    origin = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, blank=True, related_name='empty_leg_departures')
    destination = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, blank=True, related_name='empty_leg_arrivals')
    origin_raw = models.CharField(max_length=200, blank=True)
    destination_raw = models.CharField(max_length=200, blank=True)
    departure_date = models.DateField(db_index=True)
    departure_time = models.TimeField(null=True, blank=True)
    flexible_dates = models.BooleanField(default=False)
    available_until = models.DateTimeField(null=True, blank=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True)
    aircraft_raw = models.CharField(max_length=200, blank=True)
    max_passengers = models.PositiveIntegerField(null=True, blank=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    original_price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percent = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    operator_company = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True, blank=True, related_name='empty_legs')
    operator = models.CharField(max_length=200, blank=True)
    contact_info = models.TextField(blank=True)
    url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    raw_data = models.JSONField(default=dict, blank=True)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['departure_date']
        verbose_name = 'Empty Leg'
        verbose_name_plural = 'Empty Legs'
        indexes = [
            models.Index(fields=['departure_date', 'status']),
            models.Index(fields=['source', 'external_id']),
            models.Index(fields=['published', 'status', 'departure_date']),
        ]

    def __str__(self):
        origin = self.origin_raw or (str(self.origin) if self.origin else '?')
        dest = self.destination_raw or (str(self.destination) if self.destination else '?')
        return f"{origin} → {dest} ({self.departure_date})"

    @property
    def is_expired(self):
        return self.departure_date < date.today()

    def save(self, *args, **kwargs):
        # Auto-calcular descuento
        if self.price_usd and self.original_price_usd and self.original_price_usd > 0:
            self.discount_percent = round(
                float((1 - self.price_usd / self.original_price_usd) * 100), 1
            )
        # Auto-expirar
        if self.departure_date and self.departure_date < date.today() and self.status == 'available':
            self.status = 'expired'
        super().save(*args, **kwargs)


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('contacted', 'Contactado'),
        ('closed', 'Cerrado'),
    ]

    empty_leg = models.ForeignKey(EmptyLeg, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    passengers = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f"{self.name} — {self.empty_leg}"
