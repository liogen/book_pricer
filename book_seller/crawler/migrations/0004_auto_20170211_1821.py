# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_auto_20170211_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('book_condition', models.CharField(
                    blank=True, choices=[('0', 'Neuf'), ('1', 'Occassion')],
                    max_length=2, null=True)),
                ('vendor', models.CharField(blank=True, max_length=200,
                                            null=True)),
                ('country', models.CharField(blank=True, max_length=200,
                                             null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('shop_img', models.URLField(blank=True, null=True)),
                ('shop_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='book_type',
        ),
        migrations.RemoveField(
            model_name='book',
            name='country',
        ),
        migrations.RemoveField(
            model_name='book',
            name='description',
        ),
        migrations.RemoveField(
            model_name='book',
            name='price',
        ),
        migrations.RemoveField(
            model_name='book',
            name='shop_img',
        ),
        migrations.RemoveField(
            model_name='book',
            name='shop_link',
        ),
        migrations.RemoveField(
            model_name='book',
            name='vendor',
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.SlugField(max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='book',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='crawler.Book'),
        ),
    ]
