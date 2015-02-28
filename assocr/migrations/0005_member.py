# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0004_auto_20150227_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('firstsurname', models.CharField(max_length=128)),
                ('secondsurname', models.CharField(max_length=128)),
                ('dni', models.CharField(max_length=9)),
                ('birthdaydate', models.DateField()),
                ('adress', models.CharField(max_length=256)),
                ('postalcode', models.IntegerField()),
                ('city', models.CharField(max_length=128)),
                ('province', models.CharField(max_length=128)),
                ('country', models.CharField(max_length=128)),
                ('telephone', models.IntegerField()),
                ('fcbmember', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=75)),
                ('uf', models.ForeignKey(to='assocr.UF')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
