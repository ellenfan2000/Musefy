from django import forms
from django.utils import timezone


MUSEUM_CHOICE = [('MET', 'The Metropolitan Museum of Art, NYC'), ('MFA', 'Museum of Fine Arts, BOS'), ('AIC', 'The Art Institute of Chicago, CHI'), ('SNASM','Smithsonian National Air and Space Museum, DC'),('AMNH','American Museum of Natural History, NYC')]


class Query(forms.Form):
    Museum = forms.ChoiceField(label="Select Museum", widget=forms.Select, choices=MUSEUM_CHOICE)
    Time = forms.DurationField(label="How long will your Tour(in hours) be?")
    Date = forms.DateField(label="The date of your visit", initial=timezone.now, widget=forms.DateInput(attrs={'type': 'date'}))
    Curatorial = forms.CharField(label="Curatorial Area (e.g. African Art, Egyptian Art)",required=False)
    Artist = forms.CharField(label="Artists(If you have any preferred artists, list them here.)", required=False)
    Period = forms.CharField(label="Period (e.g. 1900s, 1500-1800, Renaissance)",required=False)
    Theme = forms.CharField(label="Theme(e.g. Architecture, Death, Flowers)",required=False)
    Age = forms.IntegerField(label="Age (e.g. List the youngest member in your group.)",required=False)