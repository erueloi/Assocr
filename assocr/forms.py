from django import forms
from assocr.models import Association, UF, Member
from django.contrib.auth.models import User

class AssociationForm(forms.ModelForm):
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Association
        fields = ('name', 'email', 'penyanumber', 'adress', 'city', 'telephone', 'logotype', 'url')
        
class UFForm(forms.ModelForm):
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = UF
        fields = ('currentaccount', 'typequote')
        
class MemberForm(forms.ModelForm):
    CITYCHOICES = (
               ('Lleida', 'Lleida'),
               ('Barcelona', 'Barcelona'),
               ('Alpicat', 'Alpicat'),
               ('Belloc', 'Belloc'),
               ('Raimat', 'Raimat'),
               )
    PROVINCECHOICES = (
               ('Lleida', 'Lleida'),
               ('Barcelona', 'Barcelona'),
               ('Girona', 'Girona'),
               ('Tarragona', 'Tarragona'),
               )
    COUNTRYCHOICES = (
               ('Catalunya', 'Catalunya'),
               ('Espanya', 'Espanya'),
               ('Irlanda', 'Irlanda'),
               ('Anglaterra', 'Anglaterra'),
               ('Escocia', 'Escocia'),
               )
    name = forms.CharField(max_length=128, help_text="Escrigui el seu Nom")
    firstsurname = forms.CharField(max_length=128)
    secondsurname = forms.CharField(max_length=128)
    dni = forms.CharField(max_length=9)
    birthdaydate = forms.DateInput(format='%m/%d/%Y')
    adress = forms.CharField(widget=forms.Textarea)
    postalcode = forms.IntegerField(max_value=99999)
    city = forms.ChoiceField(choices=CITYCHOICES, widget=forms.Select)
    province = forms.ChoiceField(choices=PROVINCECHOICES, widget=forms.Select)
    country = forms.ChoiceField(choices=COUNTRYCHOICES, widget=forms.Select)
    fcbmember = forms.BooleanField(required=False)
    email = forms.EmailField()
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Member
        fields = ('name', 'firstsurname', 'secondsurname', 'dni', 'birthdaydate', 'adress', 'postalcode', 'city', 'province', 'country', 'telephone', 'fcbmember', 'email')    
        