from django.contrib import admin
from import_export import resources, fields
from assocr.models import Member, UF

class MemberResource(resources.ModelResource):  
    #name = fields.Field(column_name='Nom')
    #firstsurname = fields.Field(column_name='1r Cogonom')
    
    class Meta:
        model = Member
        fields = ('uf__association__penyanumber', 'uf__currentaccount', 'uf__typequote', 'id', 'uf', 'name', 'firstsurname','secondsurname','dni',
                  'birthdaydate', 'typeadress', 'adress', 'number', 'portal', 'ladder', 'floor', 'door','postalcode', 'city', 'province', 'country', 'telephone', 'fcbmember', 'fcbnumber', 'email', )
        export_order = ('uf__association__penyanumber', 'uf__currentaccount', 'uf__typequote', 'id', 'uf', 'name', 'firstsurname','secondsurname','dni',
                  'birthdaydate', 'typeadress', 'adress', 'number', 'portal', 'ladder', 'floor', 'door','postalcode', 'city', 'province', 'country', 'telephone', 'fcbmember', 'fcbnumber', 'email', )       
         
    def before_import(self, dataset, dry_run):        
        if 'uf' in dataset.headers:
            for row in dataset.dict:
                try:
                    unif = UF.objects.get(id=int(row['uf']))
                    unif.currentaccount = row['uf__currentaccount']
                    unif.typequote = row['uf__typequote']
                    unif.save()
                except UF.DoesNotExist:
                    unif = None
                    unif = UF(id=int(row['uf']))
                    assoc = Association.objects.get(penyanumber=int(row['uf__association__penyanumber']))
                    unif.association = assoc
                    unif.state = 1
                    unif.currentaccount = row['uf__currentaccount']
                    unif.typequote = row['uf__typequote']
                    unif.save()

