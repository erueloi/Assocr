# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0003_auto_20150227_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uf',
            name='currentaccount',
            field=models.CharField(default=1, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uf',
            name='typequote',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
