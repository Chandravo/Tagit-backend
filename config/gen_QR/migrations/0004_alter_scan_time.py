# Generated by Django 4.1.5 on 2023-04-23 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gen_QR', '0003_qr_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
