# Generated by Django 4.2.6 on 2023-10-08 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0020_alter_expiringlink_image_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='base_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumbnails', to='images.image'),
        ),
    ]
