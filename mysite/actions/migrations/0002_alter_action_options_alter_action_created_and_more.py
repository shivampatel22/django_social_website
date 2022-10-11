# Generated by Django 4.1.1 on 2022-10-11 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='action',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='target_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='action',
            index=models.Index(fields=['-created'], name='actions_act_created_64f10d_idx'),
        ),
        migrations.AddIndex(
            model_name='action',
            index=models.Index(fields=['target_ct', 'target_id'], name='actions_act_target__f20513_idx'),
        ),
    ]
