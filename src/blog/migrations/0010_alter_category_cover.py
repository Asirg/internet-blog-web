# Generated by Django 4.1.5 on 2023-02-03 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='category/', verbose_name='Poster'),
        ),
    ]
