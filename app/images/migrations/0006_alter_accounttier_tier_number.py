# Generated by Django 4.2.5 on 2023-10-04 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_expiringlink_thumbnailsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttier',
            name='tier_number',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
