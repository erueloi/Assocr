# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0020_auto_20150304_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='idcalendar',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
    ]
