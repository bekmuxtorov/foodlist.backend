# Generated by Django 5.0.6 on 2025-04-25 10:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eateries', '0020_wifi_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wifi',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wifi', to='eateries.organization'),
        ),
    ]
