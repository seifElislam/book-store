# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 11:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20170425_1146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='user',
            new_name='followers',
        ),
    ]
