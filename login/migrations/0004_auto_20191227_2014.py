# Generated by Django 2.2.7 on 2019-12-27 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_articles_hotnews'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='link',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='hotnews',
            name='link',
            field=models.CharField(default='', max_length=256),
        ),
    ]
