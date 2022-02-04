# Generated by Django 4.0.1 on 2022-01-29 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0002_rename_user_id_driver_user'),
        ('riders', '0002_alter_ride_owner_order_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drivers.driver'),
        ),
        migrations.AlterField(
            model_name='ride_owner',
            name='special_requests',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ride_owner',
            name='specific_type',
            field=models.CharField(choices=[('X', 'zberX'), ('L', 'zberXL'), ('S', 'zberSUV'), ('U', 'zberLUX')], default=None, max_length=1, null=True),
        ),
    ]