# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_auto_20170927_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='items',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='items',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ecommerce.Item'),
        ),
    ]
