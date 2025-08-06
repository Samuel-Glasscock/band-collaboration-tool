from django import forms
from .models import Band

class BandCreateForm(forms.ModelForm):
    class Meta:
        model = Band
        # we only ask for “name”; slug will be auto-generated
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your band’s name",
            }),
        }
        labels = {
            "name": "Band Name",
        }
