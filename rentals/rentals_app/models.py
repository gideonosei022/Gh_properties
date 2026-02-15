from django.db import models
from django.contrib.auth.models import AbstractUser

# ------------------------------
# Custom User Model
# ------------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('owner', 'House Owner / Agent'),
        ('tenant', 'Tenant'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


# ------------------------------
# Property Listings
# ------------------------------
class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('room', 'Room'),
        ('house', 'Entire House'),
    )

    owner = models.ForeignKey('rentals_app.User', on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.location} (${self.price})"


# ------------------------------
# Property Images
# ------------------------------
class PropertyImage(models.Model):
    property = models.ForeignKey('rentals_app.Property', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


# ------------------------------
# Favorites (for Tenants)
# ------------------------------
class Favorite(models.Model):
    tenant = models.ForeignKey('rentals_app.User', on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey('rentals_app.Property', on_delete=models.CASCADE, related_name='favorited_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'property')

    def __str__(self):
        return f"{self.tenant.username} saved {self.property.title}"


# ------------------------------
# Messages between Users
# ------------------------------
class UserMessage(models.Model):
    sender = models.ForeignKey('rentals_app.User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('rentals_app.User', on_delete=models.CASCADE, related_name='received_messages')
    property = models.ForeignKey('rentals_app.Property', on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

