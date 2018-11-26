# Generated by Django 2.1.3 on 2018-11-20 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exp_models',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Run_id', models.CharField(blank=True, max_length=200)),
                ('Treatment', models.CharField(blank=True, max_length=200)),
                ('Tissue', models.CharField(blank=True, max_length=200)),
                ('Gene_id', models.CharField(blank=True, max_length=200)),
                ('Tpm', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'db_table': 'exp_data',
            },
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
