# Generated by Django 4.1.5 on 2023-01-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='describe',
            field=models.CharField(max_length=180, verbose_name='Describe'),
        ),
        migrations.AlterField(
            model_name='post',
            name='header',
            field=models.CharField(max_length=80, verbose_name='Header'),
        ),
    ]
