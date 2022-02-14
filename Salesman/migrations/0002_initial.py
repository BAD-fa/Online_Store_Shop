# Generated by Django 4.0 on 2022-01-18 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        ('Salesman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesmanProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='User.profile')),
                ('validation', models.FileField(upload_to='')),
                ('rating', models.FloatField(default=0, max_length=1)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('address', models.TextField()),
                ('postal_code', models.CharField(max_length=10)),
                ('img', models.ImageField(null=True, upload_to='salseman/profile')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('User.profile',),
        ),
        migrations.AddField(
            model_name='salesman',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Salesman.salesmanprofile'),
        ),
    ]