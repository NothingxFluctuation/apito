# Generated by Django 2.2.6 on 2020-05-15 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileman', '0019_auto_20200419_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='text',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='text1',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='text2',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='text3',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='text4',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
    ]
