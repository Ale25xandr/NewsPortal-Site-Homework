# Generated by Django 4.1.5 on 2023-03-07 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPortal', '0005_alter_post_article_alter_post_date_of_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_of_creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]