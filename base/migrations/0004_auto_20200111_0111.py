# Generated by Django 2.2.9 on 2020-01-11 01:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20200108_0258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registro',
            old_name='encabezados',
            new_name='encabezado',
        ),
        migrations.AddField(
            model_name='registro',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
