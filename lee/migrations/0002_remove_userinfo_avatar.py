# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-23 02:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='avatar',
        ),
    ]