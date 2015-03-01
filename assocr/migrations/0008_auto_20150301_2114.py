# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0007_auto_20150301_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='logotype',
            field=models.ImageField(default=b'/media/logos/nologo.png', upload_to=b'logos', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='association',
            name='name',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]
