# Generated by Django 4.1.7 on 2023-03-14 22:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant_review", "0007_remove_sms_message_body_alter_message_sms_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="title",
            field=models.TextField(blank=True, null=True),
        ),
    ]
