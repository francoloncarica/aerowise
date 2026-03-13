from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Min, Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
import hashlib

from .models import Operator, Airport, FlightSource, Aircraft, Flight, EmptyLeg, Inquiry
from .serializers import (
    OperatorSerializer, AirportSerializer, FlightSourceSerializer,
    AircraftSerializer, FlightSerializer, EmptyLegSerializer,
    EmptyLegPublicSerializer, InquirySerializer, InquiryCreateSerializer,
)


# --- Autenticación del Panel ---

def get_or_create_panel_user():
    """Obtiene o crea el usuario del panel para generar tokens."""
    user, _ = User.objects.get_or_create(
        username='aerowise_panel',
        defaults={'is_staff': True, 'is_active': True}
    )
    return user


class IsPanelAuthenticated(permissions.BasePermission):
    """Verifica que el request tenga un token válido del panel."""
    def has_permission(self, request, view):
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth.startswith('Token '):
            return False
        token_key = auth.split(' ', 1)[1]
        return Token.objects.filter(key=token_key).exists()


# --- Vistas Públicas ---

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_empty_legs(request):
    """Lista empty legs publicados SIN precios."""
    qs = EmptyLeg.objects.filter(
        published=True,
        status='available',
        departure_date__gte=timezone.now().date()
    ).select_related('origin', 'destination', 'aircraft')

    # Búsqueda por ciudad/país
    search = request.query_params.get('search', '').strip()
    if search:
        qs = qs.filter(
            Q(origin__city__icontains=search) |
            Q(origin__country__icontains=search) |
            Q(destination__city__icontains=search) |
            Q(destination__country__icontains=search) |
            Q(origin_raw__icontains=search) |
            Q(destination_raw__icontains=search)
        )

    serializer = EmptyLegPublicSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def public_create_inquiry(request):
    """Crea una consulta 'Me interesa' desde la landing."""
    serializer = InquiryCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Consulta enviada exitosamente.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Panel Auth ---

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def panel_login(request):
    """Login con contraseña única — retorna token."""
    password = request.data.get('password', '')
    if password == settings.PANEL_PASSWORD:
        user = get_or_create_panel_user()
        # Eliminar token viejo si existe y crear uno nuevo
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({'token': token.key})
    return Response({'detail': 'Contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsPanelAuthenticated])
def panel_logout(request):
    """Elimina el token actual."""
    auth = request.META.get('HTTP_AUTHORIZATION', '')
    token_key = auth.split(' ', 1)[1]
    Token.objects.filter(key=token_key).delete()
    return Response({'detail': 'Sesión cerrada.'})


@api_view(['GET'])
@permission_classes([IsPanelAuthenticated])
def panel_check(request):
    """Verifica que el token sea válido."""
    return Response({'detail': 'Autenticado.'})


# --- Panel Inquiries ---

@api_view(['GET'])
@permission_classes([IsPanelAuthenticated])
def panel_inquiries_list(request):
    """Lista consultas con filtro por status."""
    qs = Inquiry.objects.select_related('empty_leg', 'empty_leg__origin', 'empty_leg__destination').all()
    status_filter = request.query_params.get('status')
    if status_filter:
        qs = qs.filter(status=status_filter)
    serializer = InquirySerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsPanelAuthenticated])
def panel_inquiry_update(request, pk):
    """Actualiza status y admin_notes de una consulta."""
    try:
        inquiry = Inquiry.objects.get(pk=pk)
    except Inquiry.DoesNotExist:
        return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    allowed_fields = {'status', 'admin_notes'}
    for field in allowed_fields:
        if field in request.data:
            setattr(inquiry, field, request.data[field])
    inquiry.save()
    serializer = InquirySerializer(inquiry)
    return Response(serializer.data)


# --- Panel Toggle (verified/published) ---

@api_view(['PATCH'])
@permission_classes([IsPanelAuthenticated])
def panel_empty_leg_toggle(request, pk):
    """Toggle un campo: 'verified' o 'published'."""
    try:
        leg = EmptyLeg.objects.get(pk=pk)
    except EmptyLeg.DoesNotExist:
        return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    field = request.data.get('field')
    if field not in ('verified', 'published'):
        return Response({'detail': 'Campo inválido.'}, status=status.HTTP_400_BAD_REQUEST)

    current = getattr(leg, field)
    setattr(leg, field, not current)
    if field == 'verified' and not current:
        leg.verified_at = timezone.now()
    leg.save()
    serializer = EmptyLegSerializer(leg)
    return Response(serializer.data)


# --- Dashboard ---

@api_view(['GET'])
@permission_classes([IsPanelAuthenticated])
def dashboard_stats(request):
    """Estadísticas del dashboard del panel."""
    today = timezone.now().date()
    available_legs = EmptyLeg.objects.filter(status='available', departure_date__gte=today)

    total_legs = available_legs.count()
    pending_inquiries = Inquiry.objects.filter(status='pending').count()
    active_sources = FlightSource.objects.filter(is_active=True).count()

    avg_discount = available_legs.filter(
        discount_percent__isnull=False
    ).aggregate(avg=Avg('discount_percent'))['avg'] or 0

    # Leg más barato
    cheapest = available_legs.filter(
        price_usd__isnull=False
    ).order_by('price_usd').first()
    cheapest_data = None
    if cheapest:
        cheapest_data = EmptyLegSerializer(cheapest).data

    # Top rutas
    top_routes = available_legs.values(
        'origin_raw', 'destination_raw'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    # Por fuente
    by_source = available_legs.values(
        'source__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')

    # Por fecha (próximos 7 días)
    from datetime import timedelta
    by_date = []
    for i in range(7):
        d = today + timedelta(days=i)
        count = available_legs.filter(departure_date=d).count()
        by_date.append({'date': d.isoformat(), 'count': count})

    # Últimas consultas pendientes
    recent_inquiries = Inquiry.objects.filter(
        status='pending'
    ).select_related('empty_leg')[:5]
    recent_inquiries_data = InquirySerializer(recent_inquiries, many=True).data

    return Response({
        'total_legs': total_legs,
        'pending_inquiries': pending_inquiries,
        'active_sources': active_sources,
        'avg_discount': round(avg_discount, 1),
        'cheapest': cheapest_data,
        'top_routes': list(top_routes),
        'by_source': list(by_source),
        'by_date': by_date,
        'recent_inquiries': recent_inquiries_data,
    })


# --- ViewSets CRUD ---

class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
    permission_classes = [IsPanelAuthenticated]
    filterset_fields = ['company_type', 'is_active', 'country']
    search_fields = ['name', 'city', 'country']


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsPanelAuthenticated]
    filterset_fields = ['country', 'city']
    search_fields = ['icao', 'iata', 'name', 'city', 'country']


class FlightSourceViewSet(viewsets.ModelViewSet):
    queryset = FlightSource.objects.select_related('operator').all()
    serializer_class = FlightSourceSerializer
    permission_classes = [IsPanelAuthenticated]
    filterset_fields = ['source_type', 'is_active', 'operator']
    search_fields = ['name']

    @action(detail=True, methods=['post'], url_path='trigger-scrape')
    def trigger_scrape(self, request, pk=None):
        source = self.get_object()
        from .tasks import scrape_single_source
        scrape_single_source.delay(source.id)
        return Response({'detail': f'Scraping iniciado para {source.name}.'})


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_classes = [IsPanelAuthenticated]
    filterset_fields = ['category', 'manufacturer']
    search_fields = ['model', 'manufacturer']


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related('source', 'origin', 'destination', 'aircraft').all()
    serializer_class = FlightSerializer
    permission_classes = [IsPanelAuthenticated]
    filterset_fields = ['status', 'source']
    search_fields = ['flight_number', 'callsign', 'origin_raw', 'destination_raw']


class EmptyLegViewSet(viewsets.ModelViewSet):
    queryset = EmptyLeg.objects.select_related(
        'source', 'origin', 'destination', 'aircraft', 'operator_company'
    ).all()
    serializer_class = EmptyLegSerializer
    permission_classes = [IsPanelAuthenticated]
    filterset_fields = ['status', 'verified', 'published', 'source']
    search_fields = ['origin_raw', 'destination_raw', 'operator', 'aircraft_raw']
    ordering_fields = ['departure_date', 'price_usd', 'created_at', 'discount_percent']

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        leg = self.get_object()
        leg.verified = True
        leg.verified_at = timezone.now()
        leg.save()
        return Response(EmptyLegSerializer(leg).data)

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        leg = self.get_object()
        leg.published = False
        leg.save()
        return Response(EmptyLegSerializer(leg).data)
