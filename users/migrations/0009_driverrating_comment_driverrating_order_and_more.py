# Generated by Django 5.2 on 2025-04-27 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0014_review'),
        ('users', '0008_remove_artisanprofile_product_approval_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverrating',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='driverrating',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='marketplace.order'),
        ),
        migrations.AlterField(
            model_name='driverrating',
            name='rating',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='driverrating',
            unique_together={('driver', 'rated_by', 'order')},
        ),
    ]
