# Generated by Django 3.2.3 on 2021-05-28 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('Member', 'Member'), ('Convenor', 'Convenor')], max_length=200, null=True),
        ),
    ]