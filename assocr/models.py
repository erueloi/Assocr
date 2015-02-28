from django.db import models

class Association(models.Model):
    name = models.CharField(max_length=128)
    logotype = models.ImageField(upload_to='logos', blank=True)
    url = models.URLField()
    email = models.EmailField()
    penyanumber = models.IntegerField(default=0)
    adress = models.CharField(max_length=256)
    city = models.CharField(max_length=128)
    telephone = models.IntegerField()
 
    def __unicode__(self):
        return self.name + ' - ' + self.number
# 
class UF(models.Model):
    association = models.ForeignKey(Association)
    state = models.BooleanField(default=True)
    currentaccount = models.CharField(max_length=20, default=1)
    typequote = models.IntegerField(default=1)
    #number = models.IntegerField(unique=True)
 
    def __unicode__(self):
        return self.id
#     
class Member(models.Model):
    uf = models.ForeignKey(UF)
    name = models.CharField(max_length=128)
    firstsurname = models.CharField(max_length=128)
    secondsurname = models.CharField(max_length=128)
    dni = models.CharField(max_length=9)
    birthdaydate = models.DateField()
    adress = models.CharField(max_length=256)
    postalcode = models.IntegerField()
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    telephone = models.IntegerField()
    fcbmember = models.BooleanField(default=False)
    email = models.EmailField()
 
    def __unicode__(self):
        return self.name + ' ' + self.firstsurname


