# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-06-26 17:09
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=tinymce.models.HTMLField(verbose_name='Content'),
        ),
    ]
