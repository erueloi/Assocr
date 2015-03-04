# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0019_auto_20150304_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='dni',
            field=models.CharField(max_length=9, blank=True),
            preserve_default=True,
        ),
    ]
