# Generated by Django 2.2.6 on 2020-06-12 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileman', '0002_auto_20200612_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrainfo',
            name='file',
        ),
        migrations.AddField(
            model_name='extrainfo',
            name='order_no',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
