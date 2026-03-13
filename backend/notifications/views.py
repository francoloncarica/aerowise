from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import AlertSubscription
from .serializers import SubscribeSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def subscribe(request):
    """Crear suscripción de alertas."""
    serializer = SubscribeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': '¡Suscripción creada! Te avisaremos sobre nuevos empty legs.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def unsubscribe(request):
    """Desactivar suscripción por email."""
    email = request.data.get('email', '').strip()
    if not email:
        return Response({'detail': 'Email requerido.'}, status=status.HTTP_400_BAD_REQUEST)

    updated = AlertSubscription.objects.filter(email=email, is_active=True).update(is_active=False)
    if updated:
        return Response({'detail': 'Suscripción desactivada.'})
    return Response({'detail': 'No se encontró suscripción activa con ese email.'}, status=status.HTTP_404_NOT_FOUND)
