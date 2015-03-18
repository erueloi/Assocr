from django.db import models
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
    currentaccount = models.CharField(max_length=20, default=0)
 
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
    number = models.IntegerField(default=0, blank=True, null=True)
    portal = models.IntegerField(default=0, blank=True, null=True)
    ladder = models.IntegerField(default=0, blank=True, null=True)
    floor = models.IntegerField(default=0, blank=True, null=True)
    door = models.IntegerField(default=0, blank=True, null=True)
    postalcode = models.IntegerField(default=0, null=True)
    city = models.CharField(max_length=128, blank=True)
    province = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    telephone = models.IntegerField(default=0, null=True)
    fcbmember = models.BooleanField(default=False)
    fcbnumber = models.IntegerField(null=True)
    email = models.EmailField(blank=True)
  
    def __unicode__(self):
        return self.name + ' ' + self.firstsurname
    

class Receipts(models.Model):
    uf = models.ForeignKey(UF)
    year = models.IntegerField()
    state = models.IntegerField()  
    

             
            
             
     


