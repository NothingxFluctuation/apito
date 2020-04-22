# Generated by Django 2.2.6 on 2020-04-18 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileman', '0018_auto_20200416_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='file_here',
            field=models.FileField(blank=True, max_length=400, null=True, upload_to='file_content/'),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_type',
            field=models.CharField(blank=True, choices=[('im', 'Image'), ('vid', 'Video')], default='im', max_length=50),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_type1',
            field=models.CharField(blank=True, choices=[('im', 'Image'), ('vid', 'Video')], default='im', max_length=50),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_type2',
            field=models.CharField(blank=True, choices=[('im', 'Image'), ('vid', 'Video')], default='im', max_length=50),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_type3',
            field=models.CharField(blank=True, choices=[('im', 'Image'), ('vid', 'Video')], default='im', max_length=50),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_type4',
            field=models.CharField(blank=True, choices=[('im', 'Image'), ('vid', 'Video')], default='im', max_length=50),
        ),
    ]