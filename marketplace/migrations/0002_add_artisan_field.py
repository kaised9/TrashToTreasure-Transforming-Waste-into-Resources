# marketplace/migrations/0002_add_artisan_field.py

from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upcycledproduct',
            name='artisan',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                null=True,
                blank=True,
                on_delete=models.CASCADE,
                related_name='upcycled_products',
            ),
        ),
    ]
