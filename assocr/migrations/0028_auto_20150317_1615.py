# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0027_auto_20150317_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipts',
            name='year',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
