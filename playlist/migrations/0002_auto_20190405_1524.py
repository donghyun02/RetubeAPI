# Generated by Django 2.1.8 on 2019-04-05 06:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('video_id', models.CharField(max_length=32, unique=True)),
                ('thumbnail', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(max_length=32),
        ),
        migrations.AddField(
            model_name='song',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='playlist.Playlist'),
        ),
        migrations.AddIndex(
            model_name='song',
            index=models.Index(fields=['video_id'], name='playlist_so_video_i_6be463_idx'),
        ),
    ]
