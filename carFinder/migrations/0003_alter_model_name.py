# Generated by Django 4.0.5 on 2023-03-30 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carFinder', '0002_alter_brand_name_alter_model_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='name',
            field=models.CharField(max_length=80),
        ),
    ]