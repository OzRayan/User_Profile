# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-06-26 17:11
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180626_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=tinymce.models.HTMLField(),
        ),
    ]
