from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.utils.html import format_html
from .models import User, Property, PropertyImage, Message, Favorite

# ------------------------
# User Admin
# ------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    readonly_fields = ('last_login', 'date_joined')


# ------------------------
# Property Images Inline
# ------------------------
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # show one empty slot for new images
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:100px; height:auto;"/>', obj.image.url)
        return ""
    image_preview.short_description = "Preview"


# ------------------------
# Property Admin
# ------------------------
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'location', 'price', 'property_type', 'is_available', 'image_preview')
    list_filter = ('property_type', 'is_available', 'location')
    search_fields = ('title', 'location', 'owner__username')
    inlines = [PropertyImageInline]
    readonly_fields = ('created_at', 'updated_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:100px; height:auto;"/>', obj.image.url)
        return ""
    image_preview.short_description = "Main Image"


# ------------------------
# Messages Admin
# ------------------------
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('property', 'sender_name', 'sender_email', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('sender_name', 'sender_email', 'property__title')
    readonly_fields = ('sent_at',)


# ------------------------
# Favorites Admin
# ------------------------
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'property', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('tenant__username', 'property__title')
    readonly_fields = ('saved_at',)
