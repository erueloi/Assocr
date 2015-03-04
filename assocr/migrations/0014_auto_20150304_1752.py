# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0013_auto_20150304_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='uf',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]
