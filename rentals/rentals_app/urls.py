from django.urls import path
from . import views

urlpatterns = [
    # Owner auth
    path('register/', views.owner_register, name='owner_register'),
    path('login/', views.owner_login, name='owner_login'),
    path('logout/', views.owner_logout, name='owner_logout'),

    # Owner dashboard & property
    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('property/create/', views.create_property, name='create_property'),
    path('property/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('property/<int:pk>/delete/', views.delete_property, name='delete_property'),

    # Public
    path('', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),

    # Favorites
    path('favorite/<int:property_id>/', views.save_favorite, name='save_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
]

