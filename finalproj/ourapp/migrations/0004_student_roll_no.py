# Generated by Django 4.0.3 on 2022-03-12 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ourapp', '0003_rename_present_student_is_present'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='roll_no',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]