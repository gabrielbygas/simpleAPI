from django.urls import path, include
from .views import PersonsAPIView, GetContractSummary, PersonsContractAPIView



app_name = 'api'

urlpatterns = [
    path('', include('api.routers')),
    path('persons/', PersonsAPIView.as_view(), name='persons-list'),
    path('persons/<int:pk>/', PersonsAPIView.as_view(), name='persons-detail'),
    path('contracts/', GetContractSummary.as_view(), name='contract-summary'),
    path('persons/contract/', PersonsContractAPIView.as_view(), name='persons-list'),
    path('persons/contract/<int:pk>/', PersonsContractAPIView.as_view(), name='persons-detail'),
]