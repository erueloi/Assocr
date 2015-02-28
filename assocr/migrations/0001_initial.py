# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('logotype', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('url', models.URLField()),
                ('email', models.EmailField(max_length=75)),
                ('penyanumber', models.IntegerField(default=0)),
                ('adress', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=128)),
                ('telephone', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
