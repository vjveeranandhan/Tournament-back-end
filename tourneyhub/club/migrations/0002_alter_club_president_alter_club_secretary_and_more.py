# Generated by Django 5.0.7 on 2024-07-24 10:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='president',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='president_club', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='club',
            name='secretary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secretary_club', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='club',
            name='treasurer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='treasurer_club', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='club',
            name='vice_president',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vice_president_club', to=settings.AUTH_USER_MODEL),
        ),
    ]