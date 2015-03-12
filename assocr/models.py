from django.db import models
from import_export import resources, fields
from django.contrib.auth.models import User

class Association(models.Model):
    name = models.CharField(max_length=128)
    logotype = models.ImageField(upload_to='logos', blank=True)
    url = models.URLField()
    email = models.EmailField()
    penyanumber = models.IntegerField(default=0)
    adress = models.CharField(max_length=256)
    city = models.CharField(max_length=128)
    telephone = models.IntegerField()
    idcalendar = models.CharField(max_length=128, null=True)
    users = models.ManyToManyField(User)
 
    def __unicode__(self):
        return self.name + ' - ' + str(self.penyanumber)
# 
class UF(models.Model):
    association = models.ForeignKey(Association)
    state = models.BooleanField(default=True)
    currentaccount = models.CharField(max_length=20, default=1)
    typequote = models.IntegerField(default=1)
    #number = models.IntegerField(unique=True)
 
    def __unicode__(self):
        return self.id
     
class Member(models.Model):
    uf = models.ForeignKey(UF)
    name = models.CharField(max_length=128)
    firstsurname = models.CharField(max_length=128)
    secondsurname = models.CharField(max_length=128)
    dni = models.CharField(max_length=9, blank=True)
    birthdaydate = models.DateField()
    typeadress = models.CharField(max_length=128, blank=True, default='')
    adress = models.CharField(max_length=256, blank=True)
    number = models.IntegerField(default=0, blank=True)
    portal = models.IntegerField(default=0, blank=True)
    ladder = models.IntegerField(default=0, blank=True)
    floor = models.IntegerField(default=0, blank=True)
    door = models.IntegerField(default=0, blank=True)
    postalcode = models.IntegerField(default=0, null=True)
    city = models.CharField(max_length=128, blank=True)
    province = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    telephone = models.IntegerField(default=0, null=True)
    fcbmember = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
  
    def __unicode__(self):
        return self.name + ' ' + self.firstsurname
    

class Receipts(models.Model):
    uf = models.ForeignKey(UF)
    year = models.IntegerField()
    state = models.IntegerField()  
    
    
class MemberResource(resources.ModelResource):  
    class Meta:
        model = Member
        #fields = ('uf__currentaccount', )
        export_order = ('id', 'uf', 'name', 'firstsurname','secondsurname','dni',
                  'birthdaydate', 'typeadress', 'adress', 'number', 'portal', 'ladder', 'floor', 'door','postalcode', 'city', 'province', 'country', 'telephone', 'fcbmember', 'email', )       
         
    def before_import(self, dataset, dry_run):        
        if 'uf' in dataset.headers:
            for row in dataset.dict:
                try:
                    unif = UF.objects.get(id=int(row['uf']))
                    unif.currentaccount = row['currentacount']
                    unif.typequote = row['typequote']
                    unif.save()
                except UF.DoesNotExist:
                    unif = None
                    unif = UF(id=int(row['uf']))
                    assoc = Association.objects.get(penyanumber=int(row['penyanumber']))
                    unif.association = assoc
                    unif.state = 1
                    unif.currentaccount = row['currentacount']
                    unif.typequote = row['typequote']
                    unif.save()
             
            
             
     


