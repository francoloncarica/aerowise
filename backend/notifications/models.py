from django.db import models
from flights.models import EmptyLeg


class AlertSubscription(models.Model):
    FREQUENCY_CHOICES = [
        ('immediate', 'Inmediata'),
        ('daily', 'Diaria'),
        ('weekly', 'Semanal'),
    ]

    email = models.EmailField()
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    origin_keywords = models.CharField(max_length=500, blank=True, help_text='Ciudades/países de origen separados por coma')
    destination_keywords = models.CharField(max_length=500, blank=True, help_text='Ciudades/países de destino separados por coma')
    min_date = models.DateField(null=True, blank=True)
    max_date = models.DateField(null=True, blank=True)
    max_price_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aircraft_categories = models.JSONField(default=list, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Suscripción de Alerta'
        verbose_name_plural = 'Suscripciones de Alertas'

    def __str__(self):
        return f"{self.email} ({self.get_frequency_display()})"

    def matches_empty_leg(self, leg):
        """Verifica si un empty leg coincide con los criterios de la suscripción."""
        # Precio
        if self.max_price_usd and leg.price_usd and leg.price_usd > self.max_price_usd:
            return False

        # Fechas
        if self.min_date and leg.departure_date < self.min_date:
            return False
        if self.max_date and leg.departure_date > self.max_date:
            return False

        # Keywords de origen
        if self.origin_keywords:
            keywords = [k.strip().lower() for k in self.origin_keywords.split(',') if k.strip()]
            origin_text = (leg.origin_raw or '').lower()
            if leg.origin:
                origin_text += f" {leg.origin.city} {leg.origin.country}".lower()
            if not any(kw in origin_text for kw in keywords):
                return False

        # Keywords de destino
        if self.destination_keywords:
            keywords = [k.strip().lower() for k in self.destination_keywords.split(',') if k.strip()]
            dest_text = (leg.destination_raw or '').lower()
            if leg.destination:
                dest_text += f" {leg.destination.city} {leg.destination.country}".lower()
            if not any(kw in dest_text for kw in keywords):
                return False

        # Categoría de aeronave
        if self.aircraft_categories and leg.aircraft:
            if leg.aircraft.category not in self.aircraft_categories:
                return False

        return True


class NotificationLog(models.Model):
    subscription = models.ForeignKey(AlertSubscription, on_delete=models.CASCADE, related_name='logs')
    empty_leg = models.ForeignKey(EmptyLeg, on_delete=models.CASCADE, related_name='notification_logs')
    sent_at = models.DateTimeField(auto_now_add=True)
    email_subject = models.CharField(max_length=500, blank=True)
    was_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('subscription', 'empty_leg')
        ordering = ['-sent_at']
        verbose_name = 'Log de Notificación'
        verbose_name_plural = 'Logs de Notificaciones'

    def __str__(self):
        return f"{self.subscription.email} — {self.empty_leg} ({self.sent_at})"
