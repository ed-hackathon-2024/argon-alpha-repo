# Generated by Django 5.1.3 on 2024-11-09 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WealthNest', '0002_alter_user_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('category', models.TextField()),
                ('sub_category', models.TextField()),
                ('price', models.FloatField()),
                ('vat_rate', models.FloatField()),
                ('organization_id', models.TextField()),
                ('org_unit_id', models.TextField()),
                ('created_date', models.TextField()),
            ],
        ),
    ]
