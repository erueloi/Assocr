# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0015_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='adress',
            field=models.CharField(max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='city',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='country',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='postalcode',
            field=models.IntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='province',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='telephone',
            field=models.IntegerField(blank=True),
            preserve_default=True,
        ),
    ]
