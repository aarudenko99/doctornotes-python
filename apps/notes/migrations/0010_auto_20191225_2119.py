# Generated by Django 3.0 on 2019-12-25 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_draftnote_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-id',), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='note',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('status_unpublished', 'Unpublished')], default='status_unpublished', max_length=30),
        ),
    ]
