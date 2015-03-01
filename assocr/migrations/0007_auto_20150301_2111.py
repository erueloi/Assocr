# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assocr', '0006_auto_20150228_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='name',
            field=models.CharField(default=b'/media/logos/nologo.png', max_length=128),
            preserve_default=True,
        ),
    ]
