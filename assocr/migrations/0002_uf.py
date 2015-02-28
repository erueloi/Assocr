# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.BooleanField(default=True)),
                ('currentaccount', models.BigIntegerField(default=0)),
                ('typequote', models.IntegerField(default=1)),
                ('association', models.ForeignKey(to='assocr.Association')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
