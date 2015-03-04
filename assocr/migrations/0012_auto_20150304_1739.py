# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0011_auto_20150301_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=64),
            preserve_default=True,
        ),
    ]
