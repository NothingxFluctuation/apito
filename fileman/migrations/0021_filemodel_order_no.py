# Generated by Django 2.2.6 on 2020-05-15 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileman', '0020_auto_20200516_0430'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemodel',
            name='order_no',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]