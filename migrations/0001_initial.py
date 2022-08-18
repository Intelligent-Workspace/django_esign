# Generated by Django 3.2.11 on 2022-08-18 22:25

from django.db import migrations, models
import django_esign.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EsignCreds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.IntegerField()),
                ('service', models.TextField()),
                ('service_document_id', models.TextField()),
                ('creds', models.TextField()),
                ('signers', models.TextField()),
                ('signers_role', models.TextField()),
                ('signers_status', models.TextField()),
                ('flag', models.IntegerField(default=0)),
            ],
            bases=(models.Model, django_esign.models.Bitmap),
        ),
    ]