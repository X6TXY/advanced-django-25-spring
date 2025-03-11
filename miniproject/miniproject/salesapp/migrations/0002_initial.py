# Generated by Django 5.1.6 on 2025-03-11 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productsapp', '0001_initial'),
        ('salesapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='sales_rep',
            field=models.ForeignKey(limit_choices_to={'role': 'sales'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='handled_sales_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invoice',
            name='sales_order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='salesapp.salesorder'),
        ),
        migrations.AddField(
            model_name='salesorderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_items', to='productsapp.product'),
        ),
        migrations.AddField(
            model_name='salesorderitem',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_items', to='salesapp.promotion'),
        ),
        migrations.AddField(
            model_name='salesorderitem',
            name='sales_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='salesapp.salesorder'),
        ),
    ]
