# Generated by Django 4.1.1 on 2022-10-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='image',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AddIndex(
            model_name='image',
            index=models.Index(fields=['-created_at'], name='images_imag_created_62db75_idx'),
        ),
        migrations.AddIndex(
            model_name='image',
            index=models.Index(fields=['-total_likes'], name='images_imag_total_l_0bcd7e_idx'),
        ),
    ]
