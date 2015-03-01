# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0008_auto_20150301_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='logotype',
            field=models.ImageField(default=b'nologo.png', upload_to=b'logos', blank=True),
            preserve_default=True,
        ),
    ]
