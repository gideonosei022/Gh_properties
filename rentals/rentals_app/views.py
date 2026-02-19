from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Property,  PropertyImage, Message
from .forms import (
    OwnerRegistrationForm,
    OwnerLoginForm,
    PropertyForm,
    ContactOwnerForm,
    PropertySearchForm,
)
# -------------------------------
# Owner Registration
# -------------------------------
def owner_register(request):
    if request.method == "POST":
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("owner_dashboard")
    else:
        form = OwnerRegistrationForm()

    return render(request, "register.html", {"form": form})


# -------------------------------
# Owner Login
# -------------------------------
def owner_login(request):
    if request.method == "POST":
        form = OwnerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("owner_dashboard")
    else:
        form = OwnerLoginForm()

    return render(request, "login.html", {"form": form})


# -------------------------------
# Owner Logout
# -------------------------------
def owner_logout(request):
    logout(request)
    return redirect("property_list")


# -------------------------------
# Owner Dashboard & Property Management
# -------------------------------
@login_required
def owner_dashboard(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, "dashboard.html", {"properties": properties})


@login_required
def create_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)  # ✅ add request.FILES
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect("owner_dashboard")
    else:
        form = PropertyForm()

    return render(request, "property_form.html", {"form": form})





@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property)

        if form.is_valid():
            form.save()

            # ✅ Handle multiple image upload
            images = request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(property=property, image=image)

            return redirect("owner_dashboard")
    else:
        form = PropertyForm(instance=property)

    return render(request, "property_form.html", {"form": form, "property": property})




@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    property.delete()
    return redirect("owner_dashboard")


# -------------------------------
# Public Views (Guests / Tenants)
# -------------------------------
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

    return render(request, "property_list.html", {"properties": properties, "form": form})


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

    return render(request, "property_detail.html", {"property": property, "form": form})


# -------------------------------
# Session-Based Favorites (Guests)
# -------------------------------
def save_favorite(request, property_id):
    favorites = request.session.get("favorites", [])
    if property_id not in favorites:
        favorites.append(property_id)
        request.session["favorites"] = favorites
    return redirect("property_list")


def favorite_list(request):
    favorites = request.session.get("favorites", [])
    properties = Property.objects.filter(id__in=favorites)
    return render(request, "favorites.html", {"properties": properties})


