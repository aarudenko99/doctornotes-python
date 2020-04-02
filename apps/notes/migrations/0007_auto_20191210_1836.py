# Generated by Django 3.0 on 2019-12-10 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_note_draft'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='draft',
        ),
        migrations.CreateModel(
            name='DraftNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Note')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
