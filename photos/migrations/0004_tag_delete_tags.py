# Generated by Django 4.1.7 on 2023-03-04 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_remove_album_smugmug_key_remove_photo_smugmug_key_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.album')),
                ('photos', models.ManyToManyField(blank=True, to='photos.photo')),
            ],
            options={
                'unique_together': {('name', 'album')},
            },
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]