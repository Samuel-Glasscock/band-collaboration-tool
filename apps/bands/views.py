from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Band, BandMembership
from .forms import BandCreateForm

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