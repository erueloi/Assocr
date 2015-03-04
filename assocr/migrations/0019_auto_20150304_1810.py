# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0018_auto_20150304_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='telephone',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
