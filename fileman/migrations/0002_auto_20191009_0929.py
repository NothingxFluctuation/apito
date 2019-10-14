# Generated by Django 2.2.6 on 2019-10-09 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='image',
            field=models.FileField(max_length=400, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='videomodel',
            name='video',
            field=models.FileField(max_length=400, null=True, upload_to='videos/'),
        ),
    ]
