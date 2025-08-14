from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Band, BandMembership, Event
from .forms import BandCreateForm
from django.contrib import messages
from .invites import parse_invite_token
from django.core import signing
from .queries import next_event, next_event_of_kind

@login_required
def my_bands(request):
    qs = Band.objects.filter(memberships__user=request.user)
    return render(request, "bands/my_band.html", {"bands": qs})

@login_required
def create_band(request):
    if request.method == "POST":
        form = BandCreateForm(request.POST)
        if form.is_valid():
            band = form.save()
            BandMembership.objects.create(user=request.user, band=band, role="admin")
            return redirect("bands:dashboard", band_slug=band.slug)
    else:
        form = BandCreateForm()
    return render(request, "bands/create.html", {"form": form})

# stub
@login_required
def dashboard(request, band_slug):
    # only let members see the dashboard
    band = get_object_or_404(
        Band,
        slug=band_slug,
        memberships__user=request.user
    )
    return render(request, "bands/dashboard.html", {"band": band})

@login_required
def post_login_router(request):
    u = request.user
    memberships = u.bandmembership_set.select_related("band")
    if not memberships.exists():
        return redirect("band_choose")

    # If default_band is set and the user is still a member, go there
    if u.default_band_id and memberships.filter(band_id=u.default_band_id).exists():
        return redirect("band_home", slug=u.default_band.slug)

    # If exactly one membership, use it and optionally set as default (optional)
    if memberships.count() == 1:
        band = memberships.first().band
        # optional: set default once
        if not u.default_band_id:
            u.default_band = band
            u.save(update_fields=["default_band"])
        return redirect("band_home", slug=band.slug)

    # Otherwise, let them choose
    return redirect("band_choose")

@login_required
def set_current_band(request, slug):
    band = get_object_or_404(Band, slug=slug, memberships__user=request.user)
    messages.success(request, f"Switched to {band.name}.")
    return redirect("band_home", slug=band.slug)

@login_required
def set_default_band(request, slug):
    band = get_object_or_404(Band, slug=slug, memberships__user=request.user)
    request.user.default_band = band
    request.user.save(update_fields=["default_band"])
    messages.success(request, f"{band.name} is now your default band.")
    return redirect("band_choose")

@login_required
def join_via_invite(request, token):
    try:
        band_id = parse_invite_token(token)
    except signing.BadSignature:
        messages.error(request, "This invite link is invalid or expired.")
        return redirect("band_choose")
    band = get_object_or_404(Band, id=band_id)
    BandMembership.objects.get_or_create(user=request.user, band=band)
    # set default if they had none
    if not getattr(request.user.profile, "default_band_id", None):
        request.user.profile.default_band = band
        request.user.profile.save()
    request.session["current_band_id"] = band.id
    return redirect("band_home", slug=band.slug)

@login_required
def create_band(request):
    if request.method == "POST":
        name = request.POST["name"]
        band = Band.objects.create(name=name, created_by=request.user)
        BandMembership.objects.create(user=request.user, band=band, role=BandMembership.Role.ADMIN)
        # set as default if none
        if not getattr(request.user.profile, "default_band_id", None):
            request.user.profile.default_band = band
            request.user.profile.save()
        request.session["current_band_id"] = band.id
        return redirect("band_home", slug=band.slug)
    return render(request, "bands/create.html")


@login_required
def band_home(request, slug):
    band = get_object_or_404(Band, slug=slug, memberships__user=request.user)
    photos = band.photos.all()[:6]
    upcoming = next_event(band)
    next_practice = next_event_of_kind(band, Event.Kind.PRACTICE)
    next_gig = next_event_of_kind(band, Event.Kind.GIG)
    return render(request, "bands/home.html", {
        "band": band,
        "photos": photos,
        "upcoming": upcoming,
        "next_practice": next_practice,
        "next_gig": next_gig,
    })