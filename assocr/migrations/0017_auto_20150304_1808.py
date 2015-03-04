# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0016_auto_20150304_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='postalcode',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
