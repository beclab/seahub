# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-21 08:42


from django.db import migrations, models
import seahub.base.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupWiki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField(unique=True)),
                ('repo_id', models.CharField(max_length=36)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalWiki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', seahub.base.fields.LowerCaseCharField(max_length=255, unique=True)),
                ('repo_id', models.CharField(max_length=36)),
            ],
        ),
    ]
