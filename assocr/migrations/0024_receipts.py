# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0023_auto_20150310_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('state', models.IntegerField()),
                ('uf', models.ForeignKey(to='assocr.UF')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
