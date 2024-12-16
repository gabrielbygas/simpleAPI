from django.urls import path, include
from django.conf.urls.static import static
from core import settings
from .views import PersonsAPIView, GetContractSummary, PersonsContractAPIView



app_name = 'api'

urlpatterns = [
    path('', include('api.routers')),
    path('persons/', PersonsAPIView.as_view(), name='persons-list'),
    path('persons/<int:pk>/', PersonsAPIView.as_view(), name='persons-detail'),
    path('summary/', GetContractSummary.as_view(), name='summary'),
    path('persons/contract/', PersonsContractAPIView.as_view(), name='persons-list'),
    path('persons/contract/<int:pk>/', PersonsContractAPIView.as_view(), name='persons-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)