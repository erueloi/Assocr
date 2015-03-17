# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0026_member_fcbnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipts',
            name='year',
            field=models.IntegerField(unique=True),
            preserve_default=True,
        ),
    ]
