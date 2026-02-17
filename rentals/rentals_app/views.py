from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Property
from .forms import (
    OwnerRegistrationForm,
    OwnerLoginForm,
    PropertyForm,
    ContactOwnerForm,
    PropertySearchForm,
)


# =====================================================
# 🔐 OWNER AUTHENTICATION VIEWS
# =====================================================

def owner_register(request):
    if request.method == "POST":
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("owner_dashboard")
    else:
        form = OwnerRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def owner_login(request):
    if request.method == "POST":
        form = OwnerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("owner_dashboard")
    else:
        form = OwnerLoginForm()

    return render(request, "accounts/login.html", {"form": form})


def owner_logout(request):
    logout(request)
    return redirect("property_list")


# =====================================================
# 🏠 OWNER DASHBOARD & PROPERTY MANAGEMENT
# =====================================================

@login_required
def owner_dashboard(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, "accounts/dashboard.html", {
        "properties": properties
    })


@login_required
def create_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect("owner_dashboard")
    else:
        form = PropertyForm()

    return render(request, "properties/property_form.html", {
        "form": form
    })


@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == "POST":
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect("owner_dashboard")
    else:
        form = PropertyForm(instance=property)

    return render(request, "properties/property_form.html", {
        "form": form
    })


@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    property.delete()
    return redirect("owner_dashboard")


# =====================================================
# 🌍 PUBLIC PROPERTY VIEWS (NO LOGIN REQUIRED)
# =====================================================

def property_list(request):
    properties = Property.objects.filter(is_available=True)
    form = PropertySearchForm(request.GET)

    if form.is_valid():
        location = form.cleaned_data.get("location")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        property_type = form.cleaned_data.get("property_type")

        if location:
            properties = properties.filter(location__icontains=location)

        if min_price:
            properties = properties.filter(price__gte=min_price)

        if max_price:
            properties = properties.filter(price__lte=max_price)

        if property_type:
            properties = properties.filter(property_type=property_type)

    return render(request, "properties/property_list.html", {
        "properties": properties,
        "form": form
    })


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        form = ContactOwnerForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.property = property
            message.save()
            return redirect("property_detail", pk=property.pk)
    else:
        form = ContactOwnerForm()

    return render(request, "properties/property_detail.html", {
        "property": property,
        "form": form
    })


# =====================================================
# ⭐ SESSION-BASED FAVORITES (GUEST)
# =====================================================

def save_favorite(request, property_id):
    favorites = request.session.get("favorites", [])

    if property_id not in favorites:
        favorites.append(property_id)
        request.session["favorites"] = favorites

    return redirect("property_list")


def favorite_list(request):
    favorites = request.session.get("favorites", [])
    properties = Property.objects.filter(id__in=favorites)

    return render(request, "properties/favorites.html", {
        "properties": properties
    })
