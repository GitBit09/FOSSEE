from django.urls import path
from .views import (
    register, 
    login, 
    get_datasets, 
    upload_dataset,
    get_dataset_detail,
    auth_status,
    logout_view,
    generate_pdf
)

urlpatterns = [
    # Auth endpoints (matching frontend expectations)
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/status/', auth_status, name='auth_status'),
    
    # Dataset endpoints
    path('datasets/', get_datasets, name='get_datasets'),
    path('datasets/<int:dataset_id>/', get_dataset_detail, name='dataset_detail'),
    path('datasets/upload/', upload_dataset, name='upload_dataset'),
    path('datasets/<int:dataset_id>/generate_pdf/', generate_pdf, name='generate_pdf'),
]