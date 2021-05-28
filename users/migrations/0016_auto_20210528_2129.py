# Generated by Django 3.2.3 on 2021-05-28 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_userprofile_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='club',
            field=models.ForeignKey(default='None', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_club', to='users.club'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('Member', 'Member'), ('Convenor', 'Convenor')], default='Member', max_length=200, null=True),
        ),
    ]
