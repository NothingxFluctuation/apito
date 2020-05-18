# Generated by Django 2.2.6 on 2020-05-16 20:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fileman', '0021_filemodel_order_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.IntegerField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
