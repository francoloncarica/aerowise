from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'operators', views.OperatorViewSet)
router.register(r'airports', views.AirportViewSet)
router.register(r'sources', views.FlightSourceViewSet)
router.register(r'aircraft', views.AircraftViewSet)
router.register(r'flights', views.FlightViewSet)
router.register(r'empty-legs', views.EmptyLegViewSet)

urlpatterns = [
    # Públicos
    path('public/empty-legs/', views.public_empty_legs, name='public-empty-legs'),
    path('public/inquiries/', views.public_create_inquiry, name='public-create-inquiry'),
    # Panel auth
    path('panel/login/', views.panel_login, name='panel-login'),
    path('panel/logout/', views.panel_logout, name='panel-logout'),
    path('panel/check/', views.panel_check, name='panel-check'),
    # Panel inquiries
    path('panel/inquiries/', views.panel_inquiries_list, name='panel-inquiries-list'),
    path('panel/inquiries/<int:pk>/', views.panel_inquiry_update, name='panel-inquiry-update'),
    # Panel toggles
    path('panel/empty-legs/<int:pk>/toggle/', views.panel_empty_leg_toggle, name='panel-empty-leg-toggle'),
    # Dashboard
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    # CRUD
    path('', include(router.urls)),
]
