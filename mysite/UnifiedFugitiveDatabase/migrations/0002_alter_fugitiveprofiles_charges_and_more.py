# Generated by Django 4.2.5 on 2023-10-20 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UnifiedFugitiveDatabase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fugitiveprofiles',
            name='charges',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='fugitiveprofiles',
            name='details',
            field=models.TextField(),
        ),
    ]
