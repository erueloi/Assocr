from django import forms
from assocr.models import Association, UF, Member, Receipts
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

STATECHOICES = (
               ('0', 'Generat'),
               ('1', 'Enviat'),
               ('2', 'Retornat'),
               ('3', 'Pagat'),
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
    currentaccount = forms.CharField(max_length=20)
    idcalendar = forms.CharField(max_length=128)     

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Association
        fields = ('name', 'email', 'penyanumber', 'adress', 'city', 'telephone', 'logotype', 'url', 'currentaccount', 'idcalendar')
        
class User_to_AssociationForm(forms.ModelForm):
    users = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=0),required=False)
    associations = forms.ModelMultipleChoiceField(queryset=Association.objects.all(),required=False)
    associationsto = forms.MultipleChoiceField(required=False)
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Association
        fields = ('users', 'associations', 'associationsto', )
        
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
    TYPEADRESSCHOICES = (
               ('Carrer', 'Carrer'),
               ('Avinguda', 'Avinguda'),
               )
    name = forms.CharField(max_length=128, help_text="Escrigui el seu Nom")
    firstsurname = forms.CharField(max_length=128)
    secondsurname = forms.CharField(max_length=128)
    dni = forms.CharField(max_length=9) 
    birthdaydate = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    typeadress = forms.ChoiceField(choices=TYPEADRESSCHOICES, widget=forms.Select)
    adress = forms.CharField(widget=forms.Textarea)
    number = forms.IntegerField(max_value=99999)
    portal = forms.IntegerField(max_value=99999,required=False)
    ladder = forms.IntegerField(max_value=99999,required=False)
    floor = forms.IntegerField(max_value=99999,required=False)
    door = forms.IntegerField(max_value=99999,required=False)
    city = forms.ChoiceField(choices=CITYCHOICES, widget=forms.Select)
    province = forms.ChoiceField(choices=PROVINCECHOICES, widget=forms.Select)
    country = forms.ChoiceField(choices=COUNTRYCHOICES, widget=forms.Select)
    telephone = forms.IntegerField(max_value=999999999)
    fcbmember = forms.BooleanField(required=False)
    fcbnumber = forms.IntegerField(max_value=9999999)
    email = forms.EmailField()
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Member
        fields = ('name', 'firstsurname', 'secondsurname', 'dni', 'birthdaydate', 'typeadress', 'adress', 'number', 'portal', 'ladder', 'floor', 'door', 'postalcode', 'city', 'province', 'country', 'telephone', 'fcbmember', 'fcbnumber', 'email')
        
    
class ReceiptForm(forms.ModelForm):
    year = forms.IntegerField(max_value=9999)
    state = forms.ChoiceField(choices=STATECHOICES, widget=forms.RadioSelect) 
       # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Receipts
        fields = ('year', 'state')
        