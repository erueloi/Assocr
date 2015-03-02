from django import forms
from assocr.models import Association, UF, Member
from django.contrib.auth.models import User

CITYCHOICES = (
               ('Lleida', 'Lleida'),
               ('Barcelona', 'Barcelona'),
               ('Alpicat', 'Alpicat'),
               ('Belloc', 'Belloc'),
               ('Raimat', 'Raimat'),
               )

TYPEQUOTECHOICES = (
               ('1', 'Normal - 30'),
               ('2', 'Familiar - 36'),
               ('3', 'Jubilat - 15'),
               )


class AssociationForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Escrigui el seu Nom")
    email = forms.EmailField()
    penyanumber = forms.IntegerField()
    adress = forms.CharField(widget=forms.Textarea) 
    city = forms.ChoiceField(choices=CITYCHOICES, widget=forms.Select)  
    telephone = forms.IntegerField(max_value=999999999)
    logotype = forms.ImageField(required=False)
    url = forms.URLField() 
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Association
        fields = ('name', 'email', 'penyanumber', 'adress', 'city', 'telephone', 'logotype', 'url')
        
class UFForm(forms.ModelForm):
    currentaccount = forms.CharField(max_length=20)
    typequote = forms.ChoiceField(choices=TYPEQUOTECHOICES, widget=forms.RadioSelect) 
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = UF
        fields = ('currentaccount', 'typequote')
        
class MemberForm(forms.ModelForm):
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
    telephone = forms.IntegerField(max_value=999999999)
    fcbmember = forms.BooleanField(required=False)
    email = forms.EmailField()
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Member
        fields = ('name', 'firstsurname', 'secondsurname', 'dni', 'birthdaydate', 'adress', 'postalcode', 'city', 'province', 'country', 'telephone', 'fcbmember', 'email')    
        