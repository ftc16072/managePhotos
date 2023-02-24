# Generated by Django 4.1.7 on 2023-02-24 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('smugmug_key', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smugmug_key', models.CharField(max_length=16)),
                ('medium_link', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.album')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.team'),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.album')),
                ('photos', models.ManyToManyField(to='photos.photo')),
            ],
            options={
                'unique_together': {('name', 'album')},
            },
        ),
    ]
