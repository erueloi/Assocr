# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0028_auto_20150317_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='currentaccount',
            field=models.CharField(default=0, max_length=20),
            preserve_default=True,
        ),
    ]
