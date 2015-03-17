# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0025_auto_20150316_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='fcbnumber',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
