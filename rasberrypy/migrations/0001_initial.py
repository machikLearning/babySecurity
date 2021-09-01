# Generated by Django 2.1.2 on 2019-08-22 14:51

from django.db import migrations, models
import django.db.models.deletion
import rasberrypy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BabyPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=rasberrypy.models.renamingImage)),
                ('realTitle', models.CharField(max_length=200, null=True, unique=True)),
                ('fakeTitle', models.CharField(max_length=200, null=True)),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('isReverse', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BabySick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IsSick', models.BooleanField(default=False)),
                ('createTime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authentication', models.CharField(max_length=50, unique=True)),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('productKey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rasberrypy.Product')),
            ],
        ),
        migrations.AddField(
            model_name='babysick',
            name='productionKey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rasberrypy.Product'),
        ),
        migrations.AddField(
            model_name='babypicture',
            name='productionKey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rasberrypy.Product'),
        ),
    ]