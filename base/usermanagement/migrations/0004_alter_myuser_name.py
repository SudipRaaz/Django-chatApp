# Generated by Django 5.0.7 on 2024-08-08 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0003_myuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='name',
            field=models.CharField(default='name', max_length=30),
            preserve_default=False,
        ),
    ]
